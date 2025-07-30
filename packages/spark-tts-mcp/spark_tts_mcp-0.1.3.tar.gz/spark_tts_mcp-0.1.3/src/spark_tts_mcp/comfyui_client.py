import asyncio
import json
import uuid
import os
import random
import httpx
import time
import websocket
from urllib.parse import urlencode, urlparse
from pathlib import Path
import logging
from typing import Dict, Any, Optional, Tuple, Union
from datetime import datetime
import aiohttp
import aiofiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COMFYUI_API_BASE = os.getenv("COMFYUI_API_BASE", "http://192.168.3.3:8188")
logger.info(f"COMFYUI_API_BASE is set to: {COMFYUI_API_BASE}")
WS_URL = f"ws://{COMFYUI_API_BASE.split('//')[1]}/ws"
WORKFLOWS_DIR = Path(os.getenv("COMFYUI_WORKFLOWS_DIR", Path(__file__).parent / "workflows"))
DEFAULT_WORKFLOW = "spark-tts.json" # Default workflow if none specified

# --- Workflow Loading and Modification ---

def load_workflow(workflow_name: Optional[str] = None) -> Dict[str, Any]:
    """Loads a workflow JSON file from the workflows directory."""
    logger.debug(f"Attempting to load workflow: {workflow_name}")
    if workflow_name is None:
        workflow_name = DEFAULT_WORKFLOW
        logger.info(f"No workflow name provided, using default: {DEFAULT_WORKFLOW}")

    # Sanitize workflow_name to prevent directory traversal
    workflow_name = os.path.basename(workflow_name)
    if not workflow_name.endswith(".json"):
        workflow_name += ".json"

    workflow_path = WORKFLOWS_DIR / workflow_name
    if not workflow_path.is_file():
        logger.error(f"Workflow file not found: {workflow_path}")
        raise FileNotFoundError(f"Workflow file not found: {workflow_path}")

    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
            logger.info(f"Loaded workflow: {workflow_name}")
            logger.debug(f"Loaded workflow content (first 200 chars): {json.dumps(workflow, indent=2)[:200]}...")
            return workflow
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {workflow_path}: {e}")
        raise ValueError(f"Invalid JSON in workflow file: {workflow_path}")
    except Exception as e:
        logger.error(f"Error loading workflow {workflow_path}: {e}")
        raise

def find_node_by_class_type(workflow: Dict[str, Any], class_types: list[str]) -> Optional[str]:
    """Finds the first node ID matching any of the given class_types."""
    logger.debug(f"Searching for node with class_types: {class_types}")
    for node_id, node_data in workflow.items():
        if node_data.get("class_type") in class_types:
            logger.debug(f"Found node {node_id} with class_type: {node_data.get('class_type')}")
            return node_id
    logger.debug(f"No node found for class_types: {class_types}")
    return None

def find_spark_tts_adv_voice_clone_node(workflow: Dict[str, Any]) -> Optional[str]:
    """Finds the node ID for SparkTTS_AdvVoiceClone by class type."""
    SPARK_TTS_ADV_VOICE_CLONE_TYPES = [
        "SparkTTS_AdvVoiceClone",
    ]
    return find_node_by_class_type(workflow, SPARK_TTS_ADV_VOICE_CLONE_TYPES)

def find_load_audio_node(workflow: Dict[str, Any]) -> Optional[str]:
    """Finds the node ID for loading audio (e.g., LoadAudio) by class type."""
    LOAD_AUDIO_TYPES = [
        "LoadAudio",
    ]
    return find_node_by_class_type(workflow, LOAD_AUDIO_TYPES)

def find_tts_text_input_node(workflow: Dict[str, Any]) -> Optional[str]:
    """Finds the node ID for the text input (e.g., Text Multiline) by class type."""
    TEXT_INPUT_TYPES = [
        "Text Multiline",
        "WAS_Text_Input_Multiline",
    ]
    return find_node_by_class_type(workflow, TEXT_INPUT_TYPES)

def find_tts_speaker_node(workflow: Dict[str, Any]) -> Optional[str]:
    """Finds the node ID for the speaker selection (e.g., MegaTTS3SpeakersPreview) by class type."""
    SPEAKER_NODE_TYPES = [
        "MegaTTS3SpeakersPreview",
    ]
    return find_node_by_class_type(workflow, SPEAKER_NODE_TYPES)

def find_tts_run_node(workflow: Dict[str, Any]) -> Optional[str]:
    """Finds the main TTS execution node (e.g., MegaTTS3Run) by class type."""
    TTS_RUN_NODE_TYPES = [
        "MegaTTS3Run",
    ]
    return find_node_by_class_type(workflow, TTS_RUN_NODE_TYPES)

def find_audio_output_node(workflow: Dict[str, Any]) -> Optional[str]:
    """Finds the node ID for saving or previewing audio by class type."""
    AUDIO_OUTPUT_TYPES = [
        "SaveAudio",
        "PreviewAudio",
        "VAEDecodeAudio",
    ]
    return find_node_by_class_type(workflow, AUDIO_OUTPUT_TYPES)

# --- Workflow Modification Functions ---

def modify_spark_tts_workflow(
    workflow: Dict[str, Any],
    text: str,
    reference_audio_name: Optional[str] = None,
    pitch: Optional[str] = None,
    speed: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    top_k: Optional[int] = None,
    top_p: Optional[float] = None,
    reference_text: Optional[str] = None,
    batch_texts: Optional[str] = None,
    filename_prefix: Optional[str] = None,
) -> Dict[str, Any]:
    """Modifies the SparkTTS workflow with the given parameters."""
    logger.info("Starting modify_spark_tts_workflow")
    modified_workflow = workflow.copy()

    # Modify SparkTTS_AdvVoiceClone node (ID "4" in spark-tts.json)
    spark_tts_node_id = find_spark_tts_adv_voice_clone_node(modified_workflow)
    if spark_tts_node_id and "inputs" in modified_workflow[spark_tts_node_id]:
        logger.debug(f"Found SparkTTS_AdvVoiceClone node: {spark_tts_node_id}")
        inputs = modified_workflow[spark_tts_node_id]["inputs"]

        inputs["text"] = text
        logger.debug(f"Set SparkTTS_AdvVoiceClone text to: {text[:50]}...")

        if reference_text is not None:
            inputs["reference_text"] = reference_text
            logger.debug(f"Set SparkTTS_AdvVoiceClone reference_text to: {reference_text[:50]}...")
        
        if pitch is not None:
            inputs["pitch"] = pitch
            logger.debug(f"Set SparkTTS_AdvVoiceClone pitch to: {pitch}")

        if speed is not None:
            inputs["speed"] = speed
            logger.debug(f"Set SparkTTS_AdvVoiceClone speed to: {speed}")

        if max_tokens is not None:
            inputs["max_tokens"] = max_tokens
            logger.debug(f"Set SparkTTS_AdvVoiceClone max_tokens to: {max_tokens}")

        if batch_texts is not None:
            inputs["batch_texts"] = batch_texts
            logger.debug(f"Set SparkTTS_AdvVoiceClone batch_texts to: {batch_texts[:50]}...")

        if temperature is not None:
            inputs["temperature"] = temperature
            logger.debug(f"Set SparkTTS_AdvVoiceClone temperature to: {temperature}")

        if top_k is not None:
            inputs["top_k"] = top_k
            logger.debug(f"Set SparkTTS_AdvVoiceClone top_k to: {top_k}")

        if top_p is not None:
            inputs["top_p"] = top_p
            logger.debug(f"Set SparkTTS_AdvVoiceClone top_p to: {top_p}")
    else:
        logger.warning("Could not find suitable SparkTTS_AdvVoiceClone node.")

    # Modify LoadAudio node (ID "10" in spark-tts.json) for reference_audio
    if reference_audio_name:
        load_audio_node_id = find_load_audio_node(modified_workflow)
        if load_audio_node_id and "inputs" in modified_workflow[load_audio_node_id]:
            if "audio" in modified_workflow[load_audio_node_id]["inputs"]:
                modified_workflow[load_audio_node_id]["inputs"]["audio"] = reference_audio_name
                logger.info(f"Set LoadAudio node {load_audio_node_id} audio to: {reference_audio_name}")
            else:
                logger.warning(f"LoadAudio node {load_audio_node_id} does not have 'audio' input.")
        else:
            logger.warning(f"Reference audio '{reference_audio_name}' provided, but could not find suitable LoadAudio node.")
    else:
        # If no reference_audio_name is provided, ensure the LoadAudio node is either removed
        # or its connection to SparkTTS_AdvVoiceClone is severed, or its input is cleared.
        # For simplicity, we'll clear its input if it exists and is connected.
        # In ComfyUI, if a node's input is a link, setting it to a value breaks the link.
        load_audio_node_id = find_load_audio_node(modified_workflow)
        if load_audio_node_id and "inputs" in modified_workflow[load_audio_node_id]:
            if "audio" in modified_workflow[load_audio_node_id]["inputs"]:
                # Check if it's currently linked to another node (e.g., [node_id, index])
                current_audio_input = modified_workflow[load_audio_node_id]["inputs"]["audio"]
                if isinstance(current_audio_input, list):
                    # If it's a link, we can try to remove it or set it to an empty string
                    # Setting to empty string is safer as it doesn't break the workflow structure
                    modified_workflow[load_audio_node_id]["inputs"]["audio"] = ""
                    logger.info(f"Cleared LoadAudio node {load_audio_node_id} audio input as no reference_audio_name was provided.")
                elif current_audio_input: # If it's a string (e.g., a default filename)
                    modified_workflow[load_audio_node_id]["inputs"]["audio"] = ""
                    logger.info(f"Cleared LoadAudio node {load_audio_node_id} audio input (was '{current_audio_input}') as no reference_audio_name was provided.")
            else:
                logger.debug(f"LoadAudio node {load_audio_node_id} has no 'audio' input to clear.")
        else:
            logger.debug("No LoadAudio node found to clear its input.")


    # Modify SaveAudio filename_prefix (ID "11" in spark-tts.json)
    if filename_prefix is not None:
        save_audio_node_id = find_audio_output_node(modified_workflow)
        if save_audio_node_id and modified_workflow[save_audio_node_id].get("class_type") == "SaveAudio":
            if "inputs" in modified_workflow[save_audio_node_id] and "filename_prefix" in modified_workflow[save_audio_node_id]["inputs"]:
                current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                # Append current_datetime to the prefix for uniqueness
                final_prefix = f"{filename_prefix}_{current_datetime}"
                modified_workflow[save_audio_node_id]["inputs"]["filename_prefix"] = final_prefix
                logger.info(f"Set SaveAudio node {save_audio_node_id} filename_prefix to: {final_prefix}")
            else:
                logger.warning(f"SaveAudio node {save_audio_node_id} does not have 'filename_prefix' input.")
        else:
            logger.warning("Could not find suitable SaveAudio node to set filename_prefix.")
    else:
        logger.debug("No filename_prefix provided, keeping default for SaveAudio node.")

    logger.info("Finished modify_spark_tts_workflow")
    return modified_workflow

# --- ComfyUI API Interaction ---

async def upload_image_async(image_path_or_url: Union[str, bytes], client_id: str) -> str:
    """
    Uploads an image to ComfyUI's /upload/image endpoint.
    This function is kept for completeness if future workflows might need it,
    but it's not directly used by the current SparkTTS workflow.
    """
    logger.info(f"Attempting to upload image: {image_path_or_url}")
    upload_url = f"{COMFYUI_API_BASE}/upload/image"
    image_filename = "uploaded_image.png"

    async with aiohttp.ClientSession() as session:
        try:
            if isinstance(image_path_or_url, bytes):
                image_data = image_path_or_url
                logger.debug(f"Uploading image data from bytes ({len(image_data)} bytes)")
            elif isinstance(image_path_or_url, str):
                if urlparse(image_path_or_url).scheme in ['http', 'https']:
                    logger.debug(f"Downloading image from URL: {image_path_or_url}")
                    async with session.get(image_path_or_url) as resp:
                        resp.raise_for_status()
                        image_data = await resp.read()
                        logger.debug(f"Downloaded {len(image_data)} bytes from URL.")
                    image_filename = os.path.basename(urlparse(image_path_or_url).path)
                elif os.path.exists(image_path_or_url):
                    logger.debug(f"Reading image from local path: {image_path_or_url}")
                    async with aiofiles.open(image_path_or_url, 'rb') as f:
                        image_data = await f.read()
                    logger.debug(f"Read {len(image_data)} bytes from local file.")
                    image_filename = os.path.basename(image_path_or_url)
                else:
                    raise FileNotFoundError(f"Input image path or URL not found or invalid: {image_path_or_url}")
            else:
                raise ValueError(f"Unsupported image_path_or_url type: {type(image_path_or_url)}")

            form_data = aiohttp.FormData()
            form_data.add_field('image', image_data, filename=image_filename)
            form_data.add_field('overwrite', 'true')

            logger.info(f"Uploading image '{image_filename}' to {upload_url}")
            async with session.post(upload_url, data=form_data) as response:
                response.raise_for_status()
                result = await response.json()
                logger.debug(f"Upload response: {result}")

                if "name" not in result:
                    raise ValueError("Invalid response from /upload/image endpoint: 'name' missing")

                uploaded_filename = result["name"]
                logger.info(f"Image uploaded successfully as: {uploaded_filename}")
                return uploaded_filename

        except aiohttp.ClientError as e:
            logger.error(f"Network error during image upload/download: {e}")
            raise ConnectionError(f"Could not connect or download/upload image: {e}") from e
        except FileNotFoundError as e:
            logger.error(f"File error: {e}")
            raise
        except Exception as e:
            logger.exception(f"An unexpected error occurred during image upload: {e}")
            raise RuntimeError("Failed to upload image to ComfyUI") from e

async def queue_prompt_async(prompt_workflow: Dict[str, Any], client_id: str) -> str:
    """Submits a workflow to the ComfyUI queue via HTTP POST."""
    logger.info(f"Queueing prompt for client_id: {client_id}")
    os.environ['NO_PROXY'] = '127.0.0.1'
    
    payload = {"prompt": prompt_workflow, "client_id": client_id}
    headers = {'Content-Type': 'application/json'}
    url = f"{COMFYUI_API_BASE}/prompt"

    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            if "prompt_id" not in result:
                raise ValueError("Invalid response from /prompt endpoint: 'prompt_id' missing")
            logger.info(f"Queued prompt with ID: {result['prompt_id']}")
            logger.debug(f"Queue prompt response: {result}")
            return result["prompt_id"]
        except httpx.RequestError as e:
            logger.error(f"HTTP request error to {url}: {e}")
            raise ConnectionError(f"Could not connect to ComfyUI API at {url}") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from {url}: {e.response.status_code} - {e.response.text}")
            logger.debug(f"HTTP error response body: {e.response.text}")
            raise ConnectionError(f"ComfyUI API returned error: {e.response.status_code}") from e
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response from {url}: {e}")
            raise ValueError("Invalid JSON response from ComfyUI API") from e

async def get_history_async(prompt_id: str) -> Dict[str, Any]:
    """Fetches the execution history for a given prompt_id."""
    logger.info(f"Fetching history for prompt ID: {prompt_id}")
    url = f"{COMFYUI_API_BASE}/history/{prompt_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            history = response.json()
            if prompt_id not in history:
                 raise ValueError(f"Prompt ID {prompt_id} not found in history response.")
            logger.info(f"Fetched history for prompt ID: {prompt_id}")
            logger.debug(f"Raw history data for {prompt_id}: {json.dumps(history[prompt_id], indent=2)}")
            logger.info(f"Full history object received: {json.dumps(history, indent=2)}") # 添加此行以查看完整的历史记录
            return history[prompt_id]
        except httpx.RequestError as e:
            logger.error(f"HTTP request error to {url}: {e}")
            raise ConnectionError(f"Could not connect to ComfyUI API at {url}") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from {url}: {e.response.status_code} - {e.response.text}")
            logger.debug(f"HTTP error response body: {e.response.text}")
            raise ConnectionError(f"ComfyUI API returned error: {e.response.status_code}") from e
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response from {url}: {e}")
            raise ValueError("Invalid JSON response from ComfyUI API") from e

def wait_for_prompt_completion(ws_url: str, client_id: str, prompt_id: str) -> None:
    """Connects to WebSocket and waits for the execution complete signal."""
    logger.info(f"Connecting to WebSocket: {ws_url}?clientId={client_id} to wait for prompt {prompt_id}")
    uri = f"{ws_url}?clientId={client_id}"
    
    def on_message(ws, message):
        if isinstance(message, str):
            message = json.loads(message)
            msg_type = message.get('type')
            data = message.get('data', {})
            msg_prompt_id = data.get('prompt_id')

            logger.debug(f"WebSocket message received: Type={msg_type}, PromptID={msg_prompt_id}")

            if msg_type == 'status':
                status_data = data.get('status', {}).get('exec_info', {})
                logger.info(f"Queue status: {status_data}")
                
                if 'queue_remaining' in status_data and status_data['queue_remaining'] == 0:
                    ws.close()
                    logger.info("No remaining prompts in queue, closing WebSocket.")
            elif msg_type == 'progress':
                value = data.get('value', 0)
                max_val = data.get('max', 1)
                if max_val > 0 and msg_prompt_id == prompt_id:
                    logger.info(f"Progress for {prompt_id}: {value}/{max_val} ({(value/max_val)*100:.1f}%)")
            elif msg_type == 'executing':
                if data.get('node') is None and msg_prompt_id == prompt_id:
                    logger.info(f"Execution finished signal received for prompt ID: {prompt_id}")
                    ws.close()
            elif msg_type == 'execution_error' and msg_prompt_id == prompt_id:
                logger.error(f"Execution error for prompt {prompt_id}: {data}")
                raise RuntimeError(f"ComfyUI execution error: {data.get('exception_message', 'Unknown error')}")
            elif msg_type == 'execution_complete' and msg_prompt_id == prompt_id:
                logger.info(f"Execution complete signal received for prompt ID: {prompt_id}")
                ws.close()

    def on_error(ws, error):
        logger.error(f"WebSocket error: {error}")
        raise ConnectionError(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        logger.info(f"WebSocket connection closed. Status: {close_status_code}, Message: {close_msg}")

    try:
        ws = websocket.WebSocketApp(uri,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
        logger.info(f"Starting WebSocket run_forever for {prompt_id}...")
        ws.run_forever()
        logger.info(f"WebSocket run_forever for {prompt_id} finished.")
    except Exception as e:
        logger.error(f"Failed to connect to WebSocket {uri}: {e}")
        raise ConnectionError(f"Failed to connect to WebSocket {uri}") from e

def extract_audio_output_info(history: Dict[str, Any]) -> Optional[Union[Tuple[str, Optional[str]], str]]:
    """Extracts audio output information (filename, subfolder, or direct URL) from the history."""
    logger.info(f"Extracting audio output info from history.")
    logger.debug(f"Full history for audio extraction: {json.dumps(history, indent=2)}")
    if not history:
        logger.warning("History is empty, cannot extract audio output.")
        return None

    outputs_dict = None
    if "outputs" in history:
        outputs_dict = history["outputs"]
    elif history:
        # Assuming history might be {prompt_id: {outputs: ...}}
        first_prompt_id = next(iter(history))
        if "outputs" in history[first_prompt_id]:
            outputs_dict = history[first_prompt_id]["outputs"]

    if not outputs_dict:
        logger.warning("No 'outputs' section found in history for audio extraction.")
        return None

    for node_id, node_output in outputs_dict.items():
        logger.debug(f"Checking node {node_id} for audio output. Node output keys: {node_output.keys()}")
        
        # Check for SaveAudio node output structure (e.g., "audio" key with list of dicts)
        if "audio" in node_output and isinstance(node_output["audio"], list) and node_output["audio"]:
            for item in node_output["audio"]:
                if isinstance(item, dict) and item.get("type") == "output":
                    filename = item.get("filename")
                    subfolder = item.get("subfolder")
                    if filename:
                        logger.info(f"Found SaveAudio output: filename={filename}, subfolder={subfolder} from node {node_id}")
                        return filename, subfolder

        # Check for direct audio URLs or data in 'ui' (common for preview nodes like PreviewAudio)
        if "ui" in node_output and "audio" in node_output["ui"]:
            audio_data_list = node_output["ui"]["audio"]
            if audio_data_list:
                for item in audio_data_list:
                    if isinstance(item, str): # Direct URL
                        logger.info(f"Found direct audio URL in UI: {item} from node {node_id}")
                        return item
                    elif isinstance(item, dict):
                        if "url" in item:
                            logger.info(f"Found audio URL in UI dict: {item['url']} from node {node_id}")
                            return item['url']
                        elif "filename" in item:
                            filename = item.get("filename")
                            subfolder = item.get("subfolder")
                            file_type = item.get("type", "output")
                            if filename and file_type == 'output':
                                logger.info(f"Found output audio (from UI dict): filename={filename}, subfolder={subfolder} from node {node_id}")
                                return filename, subfolder
        
        # Check for a more generic 'audios' key (similar to 'images' for SaveImage)
        if "audios" in node_output and isinstance(node_output["audios"], list):
            for audio_item in node_output["audios"]:
                if isinstance(audio_item, dict) and audio_item.get("type") == "output":
                    filename = audio_item.get("filename")
                    subfolder = audio_item.get("subfolder")
                    if filename:
                        logger.info(f"Found generic 'audios' output: filename={filename}, subfolder={subfolder} from node {node_id}")
                        return filename, subfolder

    logger.warning("No audio output found in history after checking all nodes.")
    return None

async def generate_audio_async(workflow: Dict[str, Any]) -> str:
    """
    Generates audio using the provided TTS workflow and returns the preview URL or data path.
    """
    client_id = str(uuid.uuid4())
    logger.info(f"Starting audio generation with client_id: {client_id}")
    logger.debug(f"Workflow for audio generation: {json.dumps(workflow, indent=2)}")

    try:
        prompt_id = await queue_prompt_async(workflow, client_id)
        logger.info(f"Audio generation prompt queued with ID: {prompt_id}")
        
        wait_for_prompt_completion(WS_URL, client_id, prompt_id)
        logger.info(f"Audio generation prompt {prompt_id} completed.")

        history = await get_history_async(prompt_id)
        audio_output_info = extract_audio_output_info(history)

        if audio_output_info:
            if isinstance(audio_output_info, str):
                view_url = audio_output_info
                if view_url.startswith("/view") or view_url.startswith("/temp"):
                    view_url = f"{COMFYUI_API_BASE}{view_url}"
                logger.info(f"Audio generation successful. View URL: {view_url}")
                return view_url
            elif isinstance(audio_output_info, tuple):
                filename, subfolder = audio_output_info
                query_params = {"filename": filename}
                if subfolder:
                    query_params["subfolder"] = subfolder
                query_params["type"] = "output" # Assuming it's an output file
                view_url = f"{COMFYUI_API_BASE}/api/view?{urlencode(query_params)}"
                logger.info(f"Audio generation successful. View URL: {view_url}")
                return view_url
            else:
                logger.error(f"Audio generation completed but output info format is unexpected: {type(audio_output_info)}")
                raise RuntimeError("Audio generation completed but output info format is unexpected.")
        else:
            logger.error(f"Audio generation completed but no audio output found in history for prompt_id {prompt_id}.")
            logger.debug(f"Full history dump for debugging missing audio output: {json.dumps(history, indent=2)}")
            raise RuntimeError("Audio generation completed but no audio output found in history.")

    except (ConnectionError, ValueError, RuntimeError, FileNotFoundError) as e:
        logger.error(f"Audio generation failed for prompt_id {prompt_id}: {e}")
        raise
    except Exception as e:
        logger.exception(f"An unexpected error occurred during audio generation for prompt_id {prompt_id}.")
        raise RuntimeError(f"An unexpected error occurred during audio generation: {e}") from e

# Example Usage (for testing this module directly)
async def test_spark_tts_workflow():
    try:
        logger.info("Running test_spark_tts_workflow...")
        # Load and modify the spark-tts workflow
        wf = load_workflow("spark-tts.json")
        modified_wf = modify_spark_tts_workflow(
            wf, 
            text="这是一个测试文本，用于验证 SparkTTS MCP 服务器的功能。", 
            reference_audio_name="可莉_prompt.wav", # Ensure this file exists in ComfyUI's input directory
            pitch="high",
            speed="slow",
            temperature=0.9,
            filename_prefix="my_test_audio"
        )
        logger.debug(f"Modified workflow for test: {json.dumps(modified_wf, indent=2)}")

        # Generate the audio
        audio_url = await generate_audio_async(modified_wf)
        print(f"Generated Audio URL: {audio_url}")
        logger.info(f"Test completed. Generated Audio URL: {audio_url}")

    except Exception as e:
        logger.exception("Error in test_spark_tts_workflow:")
        print(f"Error in test_spark_tts_workflow: {e}")

if __name__ == "__main__":
    # Set logging level to DEBUG for detailed output during testing
    logger.setLevel(logging.DEBUG)
    # Ensure workflows directory exists for standalone testing
    if not WORKFLOWS_DIR.exists():
        WORKFLOWS_DIR.mkdir()
        print(f"Created directory: {WORKFLOWS_DIR}")
        # You might need to manually copy spark-tts.json here for standalone test
        # And ensure reference audio files are in ComfyUI's input directory

    asyncio.run(test_spark_tts_workflow())