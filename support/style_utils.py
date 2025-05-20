import json
import random
from typing import Any

import openai

from support.decorators import spinner_decorator, execution_time_decorator
from support.logger import Logger, delog

from .file_utils import save_text_to_file

ADOPT_PROMPT_TXT_PATH = "temp/02_request_to_adopt_prompt.txt"
ADOPTED_PROMPT_PATH = "temp/03_adopted_prompt.txt"
FILE_WITH_STYLES = "support/styles.json"

logger = Logger()

init_prompt_for_reformating = """Rephrase next basic idea prompt with adding style details.
PROMPT to adopt:
{}
USE next styles: {}
Style description: {}. you need to adopt prompt to this style. change background, mood, atmosphere, colors, etc.
Style palette: {}
Next is user additional requirements that you should adopt it to prompt: {}
Ensure that the output prompt should be less than 2500 char without loosing main idea and criteria."""

@spinner_decorator
def reformatIdeaPrompt(text_constant: str, *args: Any) -> str | None:
    try:
        return text_constant.format(*args)
    except KeyError as e:
        logger.log(f"Error: Missing parameter '{e.args[0]}' in the text constant.", level="ERROR")
        return None


def get_random_styles_from_file(num_of_styles: int) -> list[str]:
    with open(FILE_WITH_STYLES, "r", encoding="utf-8") as json_file:
        styles_map = json.load(json_file)
    styles = list(styles_map.keys())
    return random.sample(styles, num_of_styles)


@execution_time_decorator
def adopt_style(picture_prompt: str, style_name: str, additional_prompt: str = "") -> str | None:
    logger.log(f"\tAdopting prompt to {style_name} ...")
    with open(FILE_WITH_STYLES, "r", encoding="utf-8") as json_file:
        styles_map = json.load(json_file)
    try:
        style_description = styles_map[style_name]["description"]
        style_palette = styles_map[style_name]["palette"]
    except KeyError:
        logger.log(
            f"Error: Somme issue with style '{style_name}'. \nCheck {FILE_WITH_STYLES} file.",
            level="ERROR",
        )
        return None

    return reformatIdeaPrompt(init_prompt_for_reformating, picture_prompt, style_name, style_description, style_palette, additional_prompt)


@delog()
def generate_adopted_prompt(additional_user_prompt: str, initial_idea_prompt: str, style: str, openAIClient: openai.Client, model_to_chat: str) -> str:
    add_style = adopt_style(initial_idea_prompt, style, additional_user_prompt)
    save_text_to_file(add_style, ADOPT_PROMPT_TXT_PATH)
    logger.log(f"\tAdopting initial prompt to style {style} ...")
    adopted_prompt = get_dalle_prompt_based_on_input(openAIClient, add_style, model_to_chat)
    save_text_to_file(adopted_prompt, ADOPTED_PROMPT_PATH)
    return adopted_prompt


@delog()
@execution_time_decorator
def get_dalle_prompt_based_on_input(openAIclient: openai.Client, input_prompt: str, model_to_chat: str) -> str:
    role = "Prompt engineer for DALL·E"
    logger.log("\tGetting response from DALLE prompt generator ...")
    input_prompt = role + "\n here is user idea you need to improve and get ideal prompt" + input_prompt
    return get_prompt_result(openAIclient, input_prompt, role, model_to_chat)


@delog()
def get_prompt_result(OpenAIclient: openai.Client, input_prompt: str, gpt_role: str, model_to_chat: str) -> Any:
    completion = OpenAIclient.chat.completions.create(
        model=model_to_chat,
        messages=[{"role": "assistant", "content": input_prompt}],
    )
    return completion.choices[0].message.content


def generate_and_save_idea(prompt: str, outputfile: str, openAIclient: openai.Client, model_to_chat: str) -> str:
    idea_text = generate_idea(prompt)
    response_msg = get_prompt_result(openAIclient, idea_text, gpt_role="", model_to_chat=model_to_chat)
    save_text_to_file(response_msg, outputfile)
    return response_msg


def generate_idea(prompt: str) -> str:
    return f"Idea Summary: {prompt}"


def generate_multistyle_pictures(num_of_pictures: int, num_of_random_styles: int, list_of_styles: list[str]) -> list[str]:
    return []


def generate_picture_by_style(input_prompt: str, prompt_text: str, style: str) -> str:
    return "path_to_generated_picture.jpg"


def add_style_to_file(name: str, description: str, palette: str, file_path: str = FILE_WITH_STYLES) -> None:
    with open(file_path, "r", encoding="utf-8") as fh:
        styles = json.load(fh)
    if name in styles:
        raise ValueError(f"Style '{name}' already exists.")
    styles[name] = {"description": description, "palette": palette}
    with open(file_path, "w", encoding="utf-8") as fh:
        json.dump(styles, fh, indent=4, ensure_ascii=False)


def load_styles(file_path: str = FILE_WITH_STYLES) -> dict:
    with open(file_path, "r", encoding="utf-8") as fh:
        return json.load(fh)
