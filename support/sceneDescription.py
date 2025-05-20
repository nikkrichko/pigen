
"""
Scene Description Module

This module provides classes for generating and managing scene descriptions.
It uses Pydantic models for data validation and OpenAI's API for generating descriptions.
"""

import json
import time
from typing import Optional, List, Dict, Any, Union

from pydantic import BaseModel, ValidationError
from openai import OpenAI

from reseach.gpt_tools import GptClient
from support.logger import Logger, delog
from support.decorators import log_function_info_and_debug
from support.character_description import CharacterDescription


class SceneDescription(BaseModel):
    """Model representing a scene description."""
    scene_number: int
    description: str
    characters: List[str]
    characters_interaction: str
    setting: str
    objects: List[str]
    mood: Optional[str] = None
    time_of_day: Optional[str] = None
    weather: Optional[str] = None


class Scenes(BaseModel):
    """Model representing a collection of scenes."""
    scenes: Dict[str, SceneDescription]


class SceneGenerator:
    """
    Class for generating and managing scene descriptions.

    This class provides methods to generate scene descriptions
    using OpenAI's API and convert them to structured data.

    Attributes:
        gpt_model (str): The GPT model to use for generating descriptions.
        gpt_client (GptClient): The client for interacting with OpenAI's API.
        logger (Logger): Logger instance for logging operations.
    """

    def __init__(self, gpt_model: str = "gpt-4o-mini"):
        """
        Initialize the SceneGenerator class.

        Args:
            gpt_model (str, optional): The GPT model to use. Defaults to "gpt-4o-mini".
        """
        self.gpt_model = gpt_model
        self.gpt_client = GptClient()
        self.logger = Logger()
        self.logger.log(f"SceneGenerator initialized with model: {gpt_model}")

    @log_function_info_and_debug()
    def _convert_message_to_json(self, message) -> Dict[str, Any]:
        """
        Convert an OpenAI API message to a JSON dictionary.

        Args:
            message: The message from OpenAI API.

        Returns:
            Dict[str, Any]: The JSON dictionary representation of the scene description.
        """
        try:
            # Parse string content into dict if necessary
            if isinstance(message.content, str):
                data = json.loads(message.content)
            else:
                data = message.content

            # Create the Pydantic model instance
            scene = SceneDescription(**data)

            # Return JSON dictionary (support Pydantic v1 and v2)
            if hasattr(scene, "model_dump"):
                return scene.model_dump()
            return scene.dict()
        except (ValidationError, json.JSONDecodeError) as e:
            error_msg = f"Error converting message to JSON: {str(e)}"
            self.logger.log(error_msg)
            return {"error": error_msg}

    @delog("INFO")
    def generate_scene(self, scene_number: int, story_context: str, characters: List[str]) -> Dict[str, Any]:
        """
        Generate a scene description.

        Args:
            scene_number (int): The number of the scene to generate.
            story_context (str): The context or story segment for the scene.
            characters (List[str]): List of character names that might appear in the scene.

        Returns:
            Dict[str, Any]: The generated scene description as a JSON dictionary.
        """
        self.logger.log(f"Generating scene {scene_number} with {len(characters)} characters")

        characters_str = ", ".join(characters)
        gpt_role = "You are an expert in creating detailed scene descriptions for stories. You excel at visualizing scenes with characters, settings, and objects."
        gpt_task = f"""
        Create a detailed scene description for scene number {scene_number} based on the following context:

        Story Context:
        {story_context}

        Available Characters:
        {characters_str}

        Include only characters that are relevant to this scene. Describe their interactions, the setting, 
        objects present, mood, time of day, and weather if applicable.
        """

        try:
            client = GptClient()
            prompt_result = client.run_prompt(
                gpt_role,
                gpt_task,
                SceneDescription,
                self.gpt_model
            )

            self.logger.log(f"Successfully received response for scene {scene_number}")
            json_output = self._convert_message_to_json(prompt_result.choices[0].message)
            return json_output
        except Exception as e:
            error_msg = f"Error generating scene {scene_number}: {str(e)}"
            self.logger.log(error_msg)
            return {"error": error_msg}

    @log_function_info_and_debug()
    def save_scene_to_file(self, scene: Dict[str, Any], filename: str) -> bool:
        """
        Save a scene description to a file.

        Args:
            scene (Dict[str, Any]): The scene description.
            filename (str): The filename to save to.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json_text = json.dumps(scene, indent=4, ensure_ascii=False)
                f.write(json_text)
            self.logger.log(f"Scene description saved to {filename}")
            return True
        except Exception as e:
            self.logger.log(f"Error saving scene description to {filename}: {str(e)}")
            return False

    @delog("INFO")
    def generate_scenes_from_story(self, story_text: str, num_scenes: int, characters: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Generate multiple scene descriptions from a story.

        Args:
            story_text (str): The full story text.
            num_scenes (int): The number of scenes to generate.
            characters (List[str]): List of character names that might appear in the scenes.

        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of scene numbers to scene descriptions.
        """
        self.logger.log(f"Generating {num_scenes} scenes from story with {len(characters)} characters")

        scenes = {}
        for i in range(1, num_scenes + 1):
            scene = self.generate_scene(i, story_text, characters)
            if "error" not in scene:
                scenes[str(i)] = scene
            else:
                self.logger.log(f"Error generating scene {i}: {scene['error']}")

        return scenes
