"""
Character Appearance Module

This module provides classes for generating and managing character appearance descriptions.
It uses Pydantic models for data validation and OpenAI's API for generating descriptions.
"""

import time
import json
from typing import Optional, List, Dict, Any, Union

from pydantic import BaseModel, ValidationError
from openai import OpenAI

from reseach.gpt_tools import GptClient
from support.logger import Logger, delog
from support.decorators import log_function_info_and_debug


class Eyes(BaseModel):
    """Model representing a character's eyes."""
    shape: str
    color: str


class Hair(BaseModel):
    """Model representing a character's hair."""
    color: str
    texture: str
    length_style: str


class PhysicalAttributes(BaseModel):
    """Model representing a character's physical attributes."""
    build: str
    skin_tone: str
    height: Optional[str]
    age_range_appearance: str
    face: str
    jawline: str
    cheekbones: str
    nose: str
    lips: str
    eyes: Eyes
    brows: str
    distinguishing_marks: str
    expression_tendency: str
    hair: Hair


class PrimaryOutfit(BaseModel):
    """Model representing a character's primary outfit."""
    garment_type: str
    fit: str
    colors: List[str]
    materials: List[str]
    embroidery_symbols: str


class Overgarment(BaseModel):
    """Model representing a character's overgarment."""
    type: str
    color: str
    cut_length: str
    functionality: str


class Accessories(BaseModel):
    """Model representing a character's accessories."""
    main_item: str
    details: str
    placement: str
    symbolism: str


class CharacterDescription(BaseModel):
    """Model representing a complete character description."""
    physical_attributes: PhysicalAttributes
    primary_outfit: PrimaryOutfit
    overgarment: Optional[Overgarment]
    accessories: Accessories




class CharacterAppearance:
    """
    Class for generating and managing character appearance descriptions.

    This class provides methods to generate character appearance descriptions
    using OpenAI's API and convert them to structured data.

    Attributes:
        gpt_model (str): The GPT model to use for generating descriptions.
        gpt_client (GptClient): The client for interacting with OpenAI's API.
        logger (Logger): Logger instance for logging operations.
    """

    def __init__(self, gpt_model: str = "gpt-4o-mini"):
        """
        Initialize the CharacterAppearance class.

        Args:
            gpt_model (str, optional): The GPT model to use. Defaults to "gpt-4o-mini".
        """
        self.gpt_model = gpt_model
        self.gpt_client = GptClient()
        self.logger = Logger()
        self.logger.log(f"CharacterAppearance initialized with model: {gpt_model}")

    @log_function_info_and_debug()
    def _convert_message_to_json(self, message) -> Dict[str, Any]:
        """
        Convert an OpenAI API message to a JSON dictionary.

        Args:
            message: The message from OpenAI API.

        Returns:
            Dict[str, Any]: The JSON dictionary representation of the character description.
        """
        try:
            # Parse string content into dict if necessary
            if isinstance(message.content, str):
                data = json.loads(message.content)
            else:
                data = message.content

            # Create the Pydantic model instance
            character = CharacterDescription(**data)

            # Return JSON dictionary
            return character.model_dump()
        except (ValidationError, json.JSONDecodeError) as e:
            error_msg = f"Error converting message to JSON: {str(e)}"
            self.logger.log(error_msg)
            return {"error": error_msg}

    @delog()
    def generate_appearance(self, character_name: str) -> Dict[str, Any]:
        """
        Generate a character appearance description.

        Args:
            character_name (str): The name of the character to generate an appearance for.

        Returns:
            Dict[str, Any]: The generated character appearance description as a JSON dictionary.
        """
        self.logger.log(f"Generating appearance for character: {character_name}")

        gpt_role = "You are Expert in creating appearance description of the characters. You always use metric system. All description should be maximal historical consistent, it its applicable."
        gpt_task = f"Create character description for {character_name}"

        try:
            prompt_result = self.gpt_client.run_prompt(
                gpt_role, 
                gpt_task, 
                CharacterDescription, 
                self.gpt_model
            )

            self.logger.log(f"Successfully received response for character: {character_name}")
            json_output = self._convert_message_to_json(prompt_result.choices[0].message)
            return json_output
        except Exception as e:
            error_msg = f"Error generating appearance for {character_name}: {str(e)}"
            self.logger.log(error_msg)
            return {"error": error_msg}

    @log_function_info_and_debug()
    def save_appearance_to_file(self, appearance: Dict[str, Any], filename: str) -> bool:
        """
        Save a character appearance description to a file.

        Args:
            appearance (Dict[str, Any]): The character appearance description.
            filename (str): The filename to save to.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(appearance, f, indent=4, ensure_ascii=False)
            self.logger.log(f"Character appearance saved to {filename}")
            return True
        except Exception as e:
            self.logger.log(f"Error saving character appearance to {filename}: {str(e)}")
            return False
