# vlm_inference/inference.py
"""
The model can be loaded by a local opensource model or  call the api
Clase VLMInference: recibe imágenes: 
INPUT:

    # Single image or a list of images, because in the future maybe we want to do stitching, but for now I want just to process one 
    # Status (Optional)
devuelve JSON con:
OUTPUT:
    • actions: {type: Navigation | Interaction, parameters}  
    • description: texto descriptivo  
    • obstacles: lista de obstáculos detectados  
    • status: enum {OK, BLOCKED, ERROR, NEED_HELP} 

For now we are going just to call the api of OPENAI, But future developments it will try to call a opensource model

"""
import os
import json
import base64
import io
from enum import Enum
from typing import Dict, List, Union, TypedDict, Any
from pathlib import Path
from collections import deque
import logging # Import logging

import yaml
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import numpy as np

import time
from importlib.resources import files # For robust resource loading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Type definitions
class Status(str, Enum):
    OK = "OK"
    BLOCKED = "BLOCKED"
    ERROR = "ERROR"
    NEED_HELP = "NEED_HELP"
    FINISHED = "FINISHED"

# Updated ActionParameters to be more flexible for different action types
# For 'Navigation' type, it will contain direction, angle, distance.
# For 'Interaction' type, it will contain interaction-specific parameters.
class ActionParameters(TypedDict, total=False): # total=False means keys are optional
    direction: str
    angle: float
    distance: float
    # Potential interaction parameters (model will define these based on 'type')
    target_object: str
    interaction_type: str
    force: float
    # ... any other relevant interaction parameters

class Action(TypedDict):
    type: str # Can be "Navigation" or "Interaction"
    parameters: ActionParameters
    Goal_observed: str
    where_goal: str
    obstacle_avoidance_strategy: str # Still relevant for navigation if blocked

class InferenceResult(TypedDict):
    actions: List[Action]
    description: str
    obstacles: List[str]
    current_environment_type: str
    status: Status
    error: str # For internal use/debugging

# Type for a single item in the action history
class HistoryItem(TypedDict):
    action: Action
    description: str
    current_environment_type: str
    status: Status # Store the status of the previous step

# Configuration management
class VLMSettings:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")

class VLMInferenceError(Exception):
    """Base exception for inference errors"""
    pass

class VLMInference:
    """
    Handles visual-language model inference for navigation tasks.

    Args:
        provider: Inference provider (API or local model)
        settings: Configuration settings
        goal: The navigation goal for the VLM.
        history_size: The maximum number of past actions to store in the buffer.
    """

    def __init__(self, provider: str = "openai", settings: VLMSettings = None, goal: str=None, history_size: int = 10):
        self.settings = settings or VLMSettings()
        self.provider = provider
        self.goal = goal
        self._validate_settings()

        # Initialize action history buffer to store HistoryItem
        self.action_history: deque[HistoryItem] = deque(maxlen=history_size)
        self.base_prompt_template = self._load_base_prompt()
        self.client = self._initialize_client()
        logger.info(f"VLMInference initialized with goal: '{self.goal}', provider: '{self.provider}'")


    def _validate_settings(self) -> None:
        """Ensure required settings are present"""
        if not self.settings.api_key and self.provider == "openai":
            logger.error("OPENAI_API_KEY required for API provider")
            raise VLMInferenceError("OPENAI_API_KEY required for API provider")
        if not self.goal:
            logger.error("A 'goal' must be provided when initializing VLMInference.")
            raise VLMInferenceError("A 'goal' must be provided when initializing VLMInference.")

    def _load_base_prompt(self) -> str:
        """Load navigation prompt template from package resources without goal formatting yet"""
        try:
            # Assumes navigation_prompt.txt is in 'vlm_navigation.prompt_manager' package
            raw_prompt = files("vlm_navigation.prompt_manager").joinpath("navigation_prompt.txt").read_text()
            logger.info("Base prompt template loaded successfully.")
            return raw_prompt
        except Exception as e:
            logger.error(f"Error loading prompt: {str(e)}")
            raise VLMInferenceError(f"Error loading prompt: {str(e)}")

    def _initialize_client(self):
        """Initialize model client based on provider"""
        if self.provider == "openai":
            logger.info("Initializing OpenAI client.")
            return OpenAI(api_key=self.settings.api_key)
        # Add other providers here (e.g., local models)
        logger.error(f"Provider {self.provider} not implemented")
        raise NotImplementedError(f"Provider {self.provider} not implemented")

    def infer(self, image_input: Union[str, np.ndarray, Image.Image]) -> InferenceResult:
        """
        Perform inference on visual input.

        Args:
            image_input: Path to image, PIL Image, or numpy array

        Returns:
            Structured navigation instructions
        """
        try:
            data_url = self._process_image_input(image_input)
            logger.info("Image processed and converted to data URL.")

            # Prepare the prompt with goal and history
            current_prompt = self._prepare_prompt_with_history()
            logger.debug(f"Prompt sent to model:\n{current_prompt[:500]}...") # Log partial prompt

            response = self._call_model(data_url, current_prompt)
            logger.info("Model API call successful.")
            parsed_result = self._parse_response(response)
            logger.info(f"Model response parsed. Status: {parsed_result['status']}")

            # Store the *latest* action, description, environment type, and status in history after successful inference
            if parsed_result["status"] != Status.ERROR: # Only store if not an error
                if parsed_result["actions"]: # Ensure there's an action to store
                    self.action_history.append(HistoryItem(
                        action=parsed_result["actions"][0], # Assuming single action per turn
                        description=parsed_result["description"],
                        current_environment_type=parsed_result["current_environment_type"],
                        status=parsed_result["status"] # Store the status of this step
                    ))
                    logger.info(f"Action history updated. Current history size: {len(self.action_history)}")
                else:
                    logger.warning("No action found in parsed result, history not updated for this step.")

            return parsed_result
        except VLMInferenceError as e:
            logger.error(f"VLM Inference Error: {str(e)}")
            return self._error_result(str(e))
        except Exception as e:
            logger.exception("An unexpected error occurred during inference.") # Log full traceback
            return self._error_result(f"An unexpected error occurred: {str(e)}")

    def _prepare_prompt_with_history(self) -> str:
        """
        Formats the prompt template with the current goal and action history summary.
        The history includes previous action parameters, description, environment type, and status.
        """
        history_str = ""
        if self.action_history:
            history_str = "\nPrevious Actions Summary (most recent last):\n"
            for i, history_item in enumerate(self.action_history):
                previous_action = history_item.get("action", {})
                previous_description = history_item.get("description", "No scene description provided.")
                previous_env_type = history_item.get("current_environment_type", "N/A")
                previous_status = history_item.get("status", "N/A").value # Get the string value

                action_type = previous_action.get('type', 'N/A')
                goal_observed = previous_action.get('Goal_observed', 'N/A')
                where_goal = previous_action.get('where_goal', 'N/A')

                # Dynamically construct parameters string based on action type
                params_str = ""
                params = previous_action.get('parameters', {})
                if action_type == "Navigation":
                    direction = params.get('direction', 'N/A')
                    angle = params.get('angle', 'N/A')
                    distance = params.get('distance', 'N/A')
                    params_str = f"Direction='{direction}', Angle={angle}, Distance={distance}"
                elif action_type == "Interaction":
                    # For interaction, list all parameters found in the dictionary
                    params_str = ", ".join([f"{k}='{v}'" for k, v in params.items()])
                    if not params_str: params_str = "No specific interaction parameters."
                else:
                    params_str = "Unknown action type parameters."

                history_str += (
                    f"- Step {i+1} (Type: {action_type}, Status: {previous_status}): {params_str}. "
                    f"Goal observed: '{goal_observed}', Where: '{where_goal}'\n"
                    f"  Scene Description: '{previous_description}' (Environment: {previous_env_type})\n"
                )

        logger.debug(f"Action history for prompt: {history_str}")
        # The prompt template must contain {goal} and {action_history} placeholders.
        return self.base_prompt_template.format(goal=self.goal, action_history=history_str)


    def _process_image_input(self, image_input: Union[str, np.ndarray, Image.Image]) -> str:
        """Convert various image formats to data URL"""
        if isinstance(image_input, str):
            # Ensure path exists for local files
            if not Path(image_input).exists():
                logger.error(f"Image file not found: {image_input}")
                raise FileNotFoundError(f"Image file not found: {image_input}")
            return encode_image_to_data_url(image_input)
        elif isinstance(image_input, Image.Image):
            return pil_to_data_url(image_input)
        elif isinstance(image_input, np.ndarray):
            return array_to_data_url(image_input)
        logger.error(f"Unsupported image input type: {type(image_input)}")
        raise ValueError("Unsupported image input type")

    def _call_model(self, data_url: str, prompt_content: str) -> str:
        """Execute model inference call"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # Use the specified model
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_content},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]
                }],
                max_tokens=2048 # Set maximum response tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Model API call failed: {str(e)}", exc_info=True) # Log exception info
            raise VLMInferenceError(f"Model API call failed: {str(e)}")

    def _parse_response(self, raw_response: str) -> InferenceResult:
        """Validate and parse model response"""
        cleaned_response = raw_response.strip()
        logger.debug(f"Raw response: {raw_response}")

        # Remove markdown code block fences if present
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[len("```json"):].strip()
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-len("```")].strip()
        elif cleaned_response.startswith("```"): # Handle cases with just ```
            cleaned_response = cleaned_response[len("```"):].strip()
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-len("```")].strip()
        logger.debug(f"Cleaned response for JSON parsing: {cleaned_response[:500]}...") # Log cleaned partial response

        try:
            if not cleaned_response:
                raise VLMInferenceError("Empty response after stripping markdown. Model might have returned an empty string.")

            response_data = json.loads(cleaned_response)
            logger.debug(f"JSON parsed: {response_data}")

            # Safely parse 'status'
            status_str = response_data.get("status", Status.ERROR.value)
            try:
                parsed_status = Status(status_str)
            except ValueError:
                logger.error(f"Invalid status value in response: '{status_str}'")
                raise VLMInferenceError(f"Invalid status value in response: '{status_str}'")

            # Parse actions, ensuring they match the TypedDict structure and types
            parsed_actions = []
            for action_data in response_data.get("actions", []):
                action_type = action_data.get("type", "Navigation") # Default to Navigation

                params: ActionParameters = {}
                raw_params = action_data.get("parameters", {})

                if action_type == "Navigation":
                    params["direction"] = raw_params.get("direction", "")
                    params["angle"] = float(raw_params.get("angle", 0))
                    params["distance"] = float(raw_params.get("distance", 0.0))
                elif action_type == "Interaction":
                    # For interaction, capture all parameters as they are defined by the model
                    # The model needs to be instructed on what parameters to provide here.
                    params = raw_params # Directly assign raw parameters for interaction
                    logger.info(f"Interaction action parsed with parameters: {params}")
                else:
                    logger.warning(f"Unknown action type '{action_type}' received. Parameters may be unhandled.")
                    params = raw_params # Catch-all for unknown types

                parsed_action = Action(
                    type=action_type,
                    parameters=params,
                    Goal_observed=action_data.get("Goal_observed", "FALSE"),
                    where_goal=action_data.get("where_goal", "FALSE"),
                    obstacle_avoidance_strategy=action_data.get("obstacle_avoidance_strategy", "")
                )
                parsed_actions.append(parsed_action)

            # Get current_environment_type from response_data, with a default
            current_env_type = response_data.get("current_environment_type", "UNKNOWN_ENVIRONMENT")

            return {
                "actions": parsed_actions,
                "description": response_data.get("description", ""),
                "obstacles": response_data.get("obstacles", []),
                "current_environment_type": current_env_type,
                "status": parsed_status,
                "error": "" # No error if parsing succeeded
            }
        except json.JSONDecodeError as e:
            error_message = f"Invalid JSON response after cleaning. Original error: {str(e)}. Attempted to parse: '{cleaned_response[:200]}...'"
            logger.error(error_message, exc_info=True)
            raise VLMInferenceError(error_message)
        except Exception as e:
            # Catch any other unexpected errors during parsing and wrap them
            logger.error(f"An unexpected error occurred during response parsing: {str(e)}", exc_info=True)
            raise VLMInferenceError(f"An unexpected error occurred during response parsing: {str(e)}")

    def _error_result(self, error_msg: str) -> InferenceResult:
        """Generate a structured error result payload"""
        logger.error(f"Generating error result: {error_msg}")
        return {
            "actions": [],
            "description": f"Error during inference: {error_msg}",
            "obstacles": [],
            "current_environment_type": "UNKNOWN_ENVIRONMENT", # Default for error cases
            "status": Status.ERROR,
            "error": error_msg
        }

# Image processing utilities (kept separate as they are general purpose)
def encode_image_to_data_url(img_path: str) -> str:
    """Encode image file to base64 data URL"""
    with Image.open(img_path) as img:
        return pil_to_data_url(img)

def pil_to_data_url(img: Image.Image, format: str = "JPEG") -> str:
    """Convert PIL Image to data URL"""
    buffered = io.BytesIO()
    img.save(buffered, format=format)
    b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{format.lower()};base64,{b64}"

def array_to_data_url(arr: np.ndarray) -> str:
    """Convert numpy array to data URL"""
    img = Image.fromarray(arr)
    return pil_to_data_url(img)

# --- Example Usage ---
if __name__ == "__main__":
    # Ensure dummy image directories and files exist for the example to run.
    # The prompt file is assumed to exist and is NOT created here.

    # Create directories for dummy images if they don't exist
    dummy_image_dir = Path("./vlm_navigation/batroom_images_path_multiview/")
    dummy_image_dir.mkdir(parents=True, exist_ok=True)

    # Example image paths (ensure these paths match your actual dummy image locations)
    image_paths = [
        dummy_image_dir / "1_left.jpeg",
        dummy_image_dir / "1_left.jpeg",
        dummy_image_dir / "1_left.jpeg",
        dummy_image_dir / "1_left.jpeg",
        dummy_image_dir / "1_left.jpeg",
    ]

    # Create dummy image files if they don't exist
    for p in image_paths:
        if not p.exists():
            try:
                Image.new('RGB', (60, 30), color = 'red').save(p)
                logger.info(f"Created placeholder image: {p}")
            except Exception as e:
                logger.error(f"Could not create dummy image {p}: {e}. Please ensure Pillow (PIL) is installed ('pip install Pillow') or provide actual image files.", exc_info=True)
                # If image creation fails, you might want to skip the example or handle it differently
                break # Exit the loop if unable to create required images

    # Initialize VLMInference
    inference = VLMInference(goal="Go to the Bathroom", history_size=3)

    for i, img_path in enumerate(image_paths):
        click = time.time()
        logger.info(f"\n--- Starting Inference {i+1} with image: {img_path} ---")

        # Call infer with the image path
        result = inference.infer(str(img_path))
        clock = time.time()

        print(json.dumps(result, indent=2))
        logger.info(f"Total time for inference {i+1}: {clock-click:.2f} seconds")

        if result["actions"]:
            navigation_action = result["actions"][0]
            action_type = navigation_action.get("type")
            parameters = navigation_action.get("parameters", {})
            goal_observed = navigation_action.get("Goal_observed")
            where_goal = navigation_action.get("where_goal")
            obstacle_avoidance_strategy = navigation_action.get("obstacle_avoidance_strategy")
            current_environment_type = result.get("current_environment_type") # Get from top level
            status = result.get("status").value # Get the string value of the status

            print("\nValores desempaquetados de la última acción:")
            print(f"Tipo de acción: {action_type}")
            if action_type == "Navigation":
                direction = parameters.get("direction")
                angle = parameters.get("angle")
                distance = parameters.get("distance")
                print(f"Dirección: {direction}")
                print(f"Ángulo: {angle}")
                print(f"Distancia: {distance}")
            elif action_type == "Interaction":
                print(f"Parámetros de Interacción: {parameters}")
            print(f"Goal_observed: {goal_observed}")
            print(f"where_goal: {where_goal}")
            print(f"obstacle_avoidance_strategy: {obstacle_avoidance_strategy}")
            print(f"current_environment_type: {current_environment_type}")
            print(f"Status: {status}")
        else:
            logger.warning("No navigation action returned or an error occurred.")
            print("No navigation action returned or an error occurred.")
            if "error" in result:
                print(f"Error details: {result['error']}")
                logger.error(f"Inference error details: {result['error']}")
        print(f"Current Action History Size: {len(inference.action_history)}")
        print("---------------------------------")