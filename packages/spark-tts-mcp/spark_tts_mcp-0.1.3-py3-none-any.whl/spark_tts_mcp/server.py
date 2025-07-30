import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import Field

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base as prompt_base

# Import the client logic
try:
    from . import comfyui_client
except ImportError:
    # Allow running directly for testing or if installed as a package
    from spark_tts_mcp import comfyui_client

# Enhanced logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server with longer timeout (300 seconds)
mcp = FastMCP(
    "SparkTTS_Generator",
    version="0.1.0",
    description="MCP Server to generate speech using a local ComfyUI instance with SparkTTS.",
    timeout=300  # Increase timeout to 300 seconds (5 minutes)
)

# --- Resource Loading ---

# Dynamically load workflows as resources
workflow_dir = Path(os.getenv("COMFYUI_WORKFLOWS_DIR", Path(__file__).parent / "workflows"))

if not workflow_dir.is_dir():
    logger.warning(f"Workflows directory not found: {workflow_dir}. No workflow resources will be loaded.")
else:
    logger.info(f"Scanning for workflows in: {workflow_dir}")
    for filename in os.listdir(workflow_dir):
        if filename.endswith(".json"):
            workflow_name = filename[:-5] # Remove .json extension
            resource_uri = f"workflow://{workflow_name}"
            file_path = workflow_dir / filename

            # Define a function scope for each resource
            def create_resource_func(path: Path):
                def get_workflow_resource() -> str:
                    """Returns the content of the workflow JSON file."""
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            # Load and dump to ensure valid JSON and consistent formatting
                            content = json.load(f)
                            return json.dumps(content, indent=2)
                    except FileNotFoundError:
                        logger.error(f"Resource file not found during read: {path}")
                        return json.dumps({"error": "Workflow file not found."})
                    except json.JSONDecodeError:
                         logger.error(f"Invalid JSON in resource file: {path}")
                         return json.dumps({"error": "Invalid JSON in workflow file."})
                    except Exception as e:
                        logger.exception(f"Error reading resource file {path}: {e}")
                        return json.dumps({"error": f"Error reading workflow file: {e}"})
                return get_workflow_resource

            # Register the resource using the dynamically created function
            mcp.resource(resource_uri)(create_resource_func(file_path))
            logger.info(f"Registered resource: {resource_uri} -> {filename}")

# --- Tool Definition ---

@mcp.tool()
async def generate_spark_tts_audio(
    text: str = Field(..., description="The text to convert to speech."),
    reference_audio_name: Optional[str] = Field(None, description="Optional. The filename of the reference audio (e.g., '可莉_prompt.wav') from ComfyUI's input directory."),
    pitch: str = Field("moderate", description="Pitch of the generated speech (e.g., 'moderate', 'low', 'high')."),
    speed: str = Field("moderate", description="Speed of the generated speech (e.g., 'moderate', 'slow', 'fast')."),
    max_tokens: int = Field(3000, description="Maximum number of tokens for text processing."),
    temperature: float = Field(0.8, description="Sampling temperature for generation."),
    top_k: int = Field(50, description="Top-K sampling parameter."),
    top_p: float = Field(0.95, description="Top-P sampling parameter."),
    reference_text: Optional[str] = Field("", description="Optional reference text for voice cloning."),
    batch_texts: Optional[str] = Field("", description="Optional batch texts for generation."),
    filename_prefix: Optional[str] = Field("audio/ComfyUI", description="Prefix for the saved audio filename. A timestamp will be appended automatically.")
) -> str:
    """
    Generates audio from text using ComfyUI's SparkTTS_AdvVoiceClone workflow.

    Args:
        text: The text to convert to speech.
        reference_audio_name: Optional. The filename of the reference audio (e.g., "可莉_prompt.wav")
                              from ComfyUI's input directory.
        pitch: Pitch of the generated speech (e.g., 'moderate', 'low', 'high').
        speed: Speed of the generated speech (e.g., 'moderate', 'slow', 'fast').
        max_tokens: Maximum number of tokens for text processing.
        temperature: Sampling temperature for generation.
        top_k: Top-K sampling parameter.
        top_p: Top-P sampling parameter.
        reference_text: Optional reference text for voice cloning.
        batch_texts: Optional batch texts for generation.
        filename_prefix: Prefix for the saved audio filename. A timestamp will be appended automatically.
    Returns:
        A URL to view/download the generated audio file, or an error message.
    """
    logger.info(f"generate_spark_tts_audio called with text='{text[:50]}...', reference_audio_name='{reference_audio_name}', pitch='{pitch}', speed='{speed}', max_tokens={max_tokens}, temp={temperature}, top_k={top_k}, top_p={top_p}, filename_prefix='{filename_prefix}'")
    try:
        # 1. Load the specified workflow (spark-tts.json)
        workflow_data = comfyui_client.load_workflow("spark-tts")
        logger.info("Loaded spark-tts workflow.")

        # 2. Modify the workflow with user inputs
        modified_workflow = comfyui_client.modify_spark_tts_workflow(
            workflow=workflow_data,
            text=text,
            reference_audio_name=reference_audio_name,
            pitch=pitch,
            speed=speed,
            max_tokens=max_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            reference_text=reference_text,
            batch_texts=batch_texts,
            filename_prefix=filename_prefix
        )
        logger.info("Modified spark-tts workflow successfully.")
        
        # 3. Generate the audio using the modified workflow
        audio_url = await comfyui_client.generate_audio_async(modified_workflow)

        logger.info(f"Audio generation successful, returning URL: {audio_url}")
        return audio_url
    except FileNotFoundError as e:
        logger.error(f"Workflow file error: {e}")
        return f"Error: Workflow 'spark-tts.json' not found. Details: {e}"
    except (ConnectionError, ValueError, RuntimeError) as e:
        logger.error(f"Audio generation failed: {e}")
        return f"Error generating audio: {e}"
    except Exception as e:
        logger.exception("Unexpected error during audio generation tool execution.")
        return f"Error: An unexpected error occurred: {e}"

# --- Server Execution ---
def main():
    logger.info("main function called.") # Added log
    # Ensure the workflows directory exists relative to this script
    workflows_path = workflow_dir
    if not workflows_path.exists():
        try:
            workflows_path.mkdir(parents=True, exist_ok=True) # Use parents=True and exist_ok=True
            logger.info(f"Created missing directory: {workflows_path}")
            print(f"Created missing directory: {workflows_path}")
            print("Please ensure your workflow JSON files are placed inside this directory.")
        except Exception as e:
             logger.error(f"Failed to create workflows directory {workflows_path}: {e}")
             print(f"Error: Failed to create workflows directory {workflows_path}. Please create it manually.")

    logger.info("FastMCP instance created and server is about to start.") # Added log
    logger.info("Starting SparkTTS MCP Server...")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()