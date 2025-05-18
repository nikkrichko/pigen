import time

from gpt_tools import GptClient
from typing import Optional, List
import json
from pydantic import BaseModel, ValidationError

class Eyes(BaseModel):
    shape: str
    color: str

class Hair(BaseModel):
    color: str
    texture: str
    length_style: str

class PhysicalAttributes(BaseModel):
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
    garment_type: str
    fit: str
    colors: List[str]
    materials: List[str]
    embroidery_symbols: str

class Overgarment(BaseModel):
    type: str
    color: str
    cut_length: str
    functionality: str

class Accessories(BaseModel):
    main_item: str
    details: str
    placement: str
    symbolism: str

class CharacterDescription(BaseModel):
    physical_attributes: PhysicalAttributes
    primary_outfit: PrimaryOutfit
    overgarment: Optional[Overgarment]
    accessories: Accessories

class PromptGenerator():
    def __init__(self, gpt_model="gpt-4o-mini"):
        self.GPT_MODEL = gpt_model
        self.GPT_CLIENT = GptClient()

    def _convert_message_to_json(self,message) -> str:
        try:
            # Parse string content into dict if necessary
            if isinstance(message.content, str):
                data = json.loads(message.content)
            else:
                data = message.content

            # Create the Pydantic model instance
            character = CharacterDescription(**data)

            # Return JSON string
            # return character.model_dump_json(indent=4)
            return character.model_dump()
        except (ValidationError, json.JSONDecodeError) as e:
            return f"Error converting message to JSON: {str(e)}"

    def generate_apearence(self, character_name):
        gpt_role = "You are Expert in creating appearance description of the characters. You always use metric system. All description should be maximal historical consistent, it its aplacable. "
        gpt_task = "Create character description for " + character_name
        prompt_result = self.GPT_CLIENT.run_prompt(gpt_role, gpt_task, CharacterDescription, self.GPT_MODEL)
        message = prompt_result.choices[0].message
        # print(message)
        json_output = self._convert_message_to_json(prompt_result.choices[0].message)
        return json_output

