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

import yaml
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import numpy as np

import time
from importlib.resources import files # For robust resource loading

# Type definitions
class Status(str, Enum):
    OK = "OK"
    BLOCKED = "BLOCKED"
    ERROR = "ERROR"
    NEED_HELP = "NEED_HELP"
    FINISHED = "FINISHED"

class ActionParameters(TypedDict):
    direction: str # Now includes 'finish'
    angle: float   # Changed to float as per discussion and common practice
    distance: float

class Action(TypedDict):
    type: str
    parameters: ActionParameters
    Goal_observed: str
    where_goal: str
    obstacle_avoidance_strategy: str

class InferenceResult(TypedDict):
    actions: List[Action]
    description: str
    obstacles: List[str]
    current_environment_type: str # Added as per your prompt's output structure
    status: Status
    error: str # For internal use/debugging

# Type for a single item in the action history
class HistoryItem(TypedDict):
    action: Action # Stores the full Action TypedDict from previous step
    description: str # Stores the description from previous step
    current_environment_type: str # Store previous environment type too

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

    def _validate_settings(self) -> None:
        """Ensure required settings are present"""
        if not self.settings.api_key and self.provider == "openai":
            raise VLMInferenceError("OPENAI_API_KEY required for API provider")
        if not self.goal:
            raise VLMInferenceError("A 'goal' must be provided when initializing VLMInference.")

    def _load_base_prompt(self) -> str:
        """Load navigation prompt template from package resources without goal formatting yet"""
        try:
            # Assumes navigation_prompt.txt is in 'vlm_navigation.prompt_manager' package
            raw_prompt = files("vlm_navigation.prompt_manager").joinpath("navigation_prompt.txt").read_text()
            return raw_prompt
        except Exception as e:
            raise VLMInferenceError(f"Error loading prompt: {str(e)}")

    def _initialize_client(self):
        """Initialize model client based on provider"""
        if self.provider == "openai":
            return OpenAI(api_key=self.settings.api_key)
        # Add other providers here (e.g., local models)
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
            
            # Prepare the prompt with goal and history
            current_prompt = self._prepare_prompt_with_history()

            response = self._call_model(data_url, current_prompt)
            parsed_result = self._parse_response(response)
            
            # Store the *latest* action, description, and environment type in history after successful inference
            # Only store if actions are present and status is not ERROR (to avoid storing invalid steps)
            if parsed_result["actions"] and parsed_result["status"] != Status.ERROR:
                self.action_history.append(HistoryItem(
                    action=parsed_result["actions"][0], # Assuming single action per turn
                    description=parsed_result["description"], # Store the description
                    current_environment_type=parsed_result["current_environment_type"] # Store environment type
                ))

            return parsed_result
        except Exception as e:
            # Catch any high-level exceptions and return an error result
            return self._error_result(str(e))

    def _prepare_prompt_with_history(self) -> str:
        """
        Formats the prompt template with the current goal and action history summary.
        The history includes previous action parameters, description, and environment type.
        """
        history_str = ""
        if self.action_history:
            history_str = "\nPrevious Actions Summary (most recent last):\n"
            for i, history_item in enumerate(self.action_history):
                previous_action = history_item.get("action", {})
                previous_description = history_item.get("description", "No scene description provided.")
                previous_env_type = history_item.get("current_environment_type", "N/A")

                direction = previous_action.get('parameters', {}).get('direction', 'N/A')
                angle = previous_action.get('parameters', {}).get('angle', 'N/A')
                distance = previous_action.get('parameters', {}).get('distance', 'N/A')
                action_type = previous_action.get('type', 'N/A')
                goal_observed = previous_action.get('Goal_observed', 'N/A')
                where_goal = previous_action.get('where_goal', 'N/A')
                
                history_str += (
                    f"- Step {i+1} (Type: {action_type}): Direction='{direction}', Angle={angle}, Distance={distance}. "
                    f"Goal observed: '{goal_observed}', Where: '{where_goal}'\n"
                    f"  Scene Description: '{previous_description}' (Environment: {previous_env_type})\n"
                )
        
        # The prompt template must contain {goal} and {action_history} placeholders.
        return self.base_prompt_template.format(goal=self.goal, action_history=history_str)


    def _process_image_input(self, image_input: Union[str, np.ndarray, Image.Image]) -> str:
        """Convert various image formats to data URL"""
        if isinstance(image_input, str):
            # Ensure path exists for local files
            if not Path(image_input).exists():
                raise FileNotFoundError(f"Image file not found: {image_input}")
            return encode_image_to_data_url(image_input)
        elif isinstance(image_input, Image.Image):
            return pil_to_data_url(image_input)
        elif isinstance(image_input, np.ndarray):
            return array_to_data_url(image_input)
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
            raise VLMInferenceError(f"Model API call failed: {str(e)}")

    def _parse_response(self, raw_response: str) -> InferenceResult:
            """Validate and parse model response"""
            cleaned_response = raw_response.strip()

            # Remove markdown code block fences if present
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[len("```json"):].strip()
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-len("```")].strip()
            elif cleaned_response.startswith("```"): # Handle cases with just ```
                cleaned_response = cleaned_response[len("```"):].strip()
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-len("```")].strip()

            try:
                if not cleaned_response:
                    raise VLMInferenceError("Empty response after stripping markdown. Model might have returned an empty string.")

                response_data = json.loads(cleaned_response)

                # Safely parse 'status'
                status_str = response_data.get("status", Status.ERROR.value)
                try:
                    parsed_status = Status(status_str)
                except ValueError:
                    raise VLMInferenceError(f"Invalid status value in response: '{status_str}'")

                # Parse actions, ensuring they match the TypedDict structure and types
                parsed_actions = []
                for action_data in response_data.get("actions", []):
                    params = action_data.get("parameters", {})
                    parsed_action = Action(
                        type=action_data.get("type", "Navigation"), # Default type
                        parameters=ActionParameters(
                            direction=params.get("direction", ""),
                            angle=float(params.get("angle", 0)), # Ensure float, default 0.0
                            distance=float(params.get("distance", 0.0)) # Ensure float, default 0.0
                        ),
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
                raise VLMInferenceError(error_message)
            except Exception as e:
                # Catch any other unexpected errors during parsing and wrap them
                raise VLMInferenceError(f"An unexpected error occurred during response parsing: {str(e)}")

    def _error_result(self, error_msg: str) -> InferenceResult:
        """Generate a structured error result payload"""
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
        dummy_image_dir / "2_center.jpeg",
        dummy_image_dir / "3_right.jpeg",
        dummy_image_dir / "4_center.jpeg",
        dummy_image_dir / "5_center.jpeg", 
    ]

    # Create dummy image files if they don't exist
    for p in image_paths:
        if not p.exists():
            try:
                Image.new('RGB', (60, 30), color = 'red').save(p)
                print(f"Created placeholder image: {p}")
            except Exception as e:
                print(f"Could not create dummy image {p}: {e}. Please ensure Pillow (PIL) is installed ('pip install Pillow') or provide actual image files.")
                # If image creation fails, you might want to skip the example or handle it differently
                break # Exit the loop if unable to create required images

    # Initialize VLMInference
    inference = VLMInference(goal="Go to the Bathroom", history_size=3) 
    
    for i, img_path in enumerate(image_paths):
        click = time.time()
        print(f"\n--- Inference {i+1} with image: {img_path} ---")
        
        # Call infer with the image path
        result = inference.infer(str(img_path)) 
        clock = time.time()
        
        print(json.dumps(result, indent=2))
        print(f"Total time with the API: {clock-click:.2f} seconds")

        if result["actions"]:
            navigation_action = result["actions"][0]
            action_type = navigation_action.get("type")
            parameters = navigation_action.get("parameters", {})
            direction = parameters.get("direction")
            angle = parameters.get("angle")
            distance = parameters.get("distance")
            goal_observed = navigation_action.get("Goal_observed")
            where_goal = navigation_action.get("where_goal")
            obstacle_avoidance_strategy = navigation_action.get("obstacle_avoidance_strategy")
            current_environment_type = result.get("current_environment_type") # Get from top level

            print("\nValores desempaquetados de la última acción:")
            print(f"Tipo de acción: {action_type}")
            print(f"Dirección: {direction}")
            print(f"Ángulo: {angle}")
            print(f"Distancia: {distance}")
            print(f"Goal_observed: {goal_observed}")
            print(f"where_goal: {where_goal}")
            print(f"obstacle_avoidance_strategy: {obstacle_avoidance_strategy}")
            print(f"current_environment_type: {current_environment_type}")
        else:
            print("No navigation action returned or an error occurred.")
            if "error" in result:
                print(f"Error details: {result['error']}")
        print(f"Current Action History Size: {len(inference.action_history)}")
        print("---------------------------------")