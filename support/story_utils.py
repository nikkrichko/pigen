import json
import datetime
from typing import Any, Dict, List, Optional

import openai

from support.logger import Logger, delog
from support.decorators import log_function_info_and_debug

logger = Logger()


@delog()
@log_function_info_and_debug()
def validate_story(text: str, openai_client: openai.Client, model: str) -> Dict[str, Any]:
    """Validate that ``text`` is a narrative suitable for illustration."""
    prompt = f"""
    Analyze the following text and determine if it's a narrative story that can be illustrated.

    Text to analyze:
    {text}

    Respond in JSON format with keys is_story, reason and estimated_scenes.
    """
    try:
        completion = openai_client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a literary analyst."},
                {"role": "user", "content": prompt},
            ],
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        logger.log(f"Error validating story: {e}", level="ERROR")
        return {"is_story": False, "reason": f"Error during validation: {e}", "estimated_scenes": 0}


@delog()
@log_function_info_and_debug()
def extract_characters(text: str, openai_client: openai.Client, model: str) -> Dict[str, Dict[str, Any]]:
    prompt = f"""
    Analyze the following story and identify all characters. Just list the character names without any descriptions.

    Story:
    {text}

    Respond in JSON format with an array of character names:
    {{"characters": ["Character Name 1", "Character Name 2"]}}
    """
    try:
        completion = openai_client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a character analyst."},
                {"role": "user", "content": prompt},
            ],
        )
        characters_list = json.loads(completion.choices[0].message.content)
        from support.character_description import CharacterAppearance
        ca = CharacterAppearance(gpt_model=model)
        result = {}
        for character_name in characters_list.get("characters", []):
            result[character_name] = ca.generate_appearance(character_name)
            filename = f"temp/{character_name.replace(' ', '_').lower()}_appearance.json"
            ca.save_appearance_to_file(result[character_name], filename)
        return result
    except Exception as e:
        logger.log(f"Error extracting characters: {e}", level="ERROR")
        return {}


@delog()
@log_function_info_and_debug()
def load_characters_from_file(file_path: str) -> Optional[Dict[str, Any]]:
    logger.log(f"Loading characters from {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError("Character file must contain a JSON object")
        from support.character_description import CharacterDescription
        validated: Dict[str, Any] = {}
        for name, desc in data.items():
            if hasattr(CharacterDescription, "model_validate"):
                obj = CharacterDescription.model_validate(desc)
                validated[name] = obj.model_dump()
            else:
                obj = CharacterDescription(**desc)
                validated[name] = obj.dict()
        return validated
    except Exception as e:
        logger.log(f"Error loading characters from file: {e}", level="ERROR")
        return None


@delog()
@log_function_info_and_debug()
def generate_scenes(text: str, num_scenes: int, characters: Dict[str, Dict[str, str]], openai_client: openai.Client, model: str) -> List[Dict[str, Any]]:
    try:
        character_names = list(characters.keys())
        from support.sceneDescription import SceneGenerator
        scene_generator = SceneGenerator(gpt_model=model)
        scenes_dict = scene_generator.generate_scenes_from_story(text, num_scenes, character_names)
        scenes_list = []
        for scene_number, scene_data in scenes_dict.items():
            scene_data_copy = scene_data.copy()
            scene_data_copy["scene_number"] = int(scene_number)
            scenes_list.append(scene_data_copy)
        return scenes_list
    except Exception as e:
        logger.log(f"Error generating scenes: {e}", level="ERROR")
        return []


def create_story_illustration_json(story_text: str, characters: Dict[str, Dict[str, str]], scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
    story_summary = story_text[:200] + "..." if len(story_text) > 200 else story_text
    return {
        "story_summary": story_summary,
        "characters": characters,
        "scenes": scenes,
        "metadata": {
            "generated_at": datetime.datetime.now().isoformat(),
            "num_scenes": len(scenes),
            "num_characters": len(characters),
        },
    }


@delog()
@log_function_info_and_debug()
def illustrate_story(story_text: str, output_file: str, num_scenes: int, openai_client: openai.Client, model: str, charfile: Optional[str] = None) -> Optional[str]:
    logger.log(f"Starting story illustration process for {len(story_text)} characters of text")
    if charfile:
        characters = load_characters_from_file(charfile)
        if not characters:
            logger.log("Invalid character file provided", level="ERROR")
            return None
    else:
        logger.log("Extracting characters from story")
        characters = extract_characters(story_text, openai_client, model)
    if not characters:
        logger.log("Failed to extract characters from the story")
        return None
    logger.log(f"Generating {num_scenes} scenes from story")
    scenes = generate_scenes(story_text, num_scenes, characters, openai_client, model)
    if not scenes:
        logger.log("Failed to generate scenes from the story")
        return None
    result = create_story_illustration_json(story_text, characters, scenes)
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.log(f"Story illustration saved to {output_file}")
        return output_file
    except Exception as e:
        logger.log(f"Error saving output file: {e}")
        return None
