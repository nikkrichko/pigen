import time

import requests
import json
import os
import requests
from openai import OpenAI
from icecream import ic
import datetime
from pprint import pprint as pp
from pprint import pprint as pp




def execution_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\t\tExecution time for '{func.__name__}': {execution_time:.2f} seconds")
        return result
    return wrapper

@execution_time_decorator
def generate_image(picture_prompt, opneai_client, model="dall-e-3", size="1024x1024", quality="standard", num_of_pics=1):
    global response
    print("\tGenerating image ...")
    response = opneai_client.images.generate(
        model=model,
        prompt=picture_prompt,
        size=size,
        quality=quality,
        n=num_of_pics,
    )
    image_url = response.data[0].url
    bin_picture = requests.get(image_url)
    return bin_picture.content

def save_picture(file_name, picture):
    print("\t\tsaving image ...")
    file = open(file_name, "wb")
    file.write(picture)
    file.close()
    print(f"\t\tImage saved to {file_name}.")


def save_text_to_file(text, filename):
    print("\t\tSaving text ...")
    with open(filename, 'w', encoding='utf-8', errors='replace') as file:
        file.write(text)
    print(f"\t\tText saved to {filename}.")

init_prompt_for_reformating = """
Rephrase next basic idea prompt with adding style details.
think about it at this prompt at first. it should pass all next criteria:
ensure that output prompt should be less than 2500 char without loosing main idea and criteria.
ensure that the output prompt adheres to DALL-E 3's policy limitations while preserving the main idea and criteria. 
Add as much details as possible. 
Provide a comprehensive description for the main subject of the picture, including intricate details of their appearance, pose, expression, attire, and any relevant surroundings or props. The goal is to create a vivid and immersive visual description that leaves no aspect of the subject to the imagination.
Add background description according to the style. but background should contain also a lot of details but it should not distract from the main subject of the picture or illustration
you need also to describe Mood and Atmosphere: Convey the overall mood or atmosphere of the illustration, including color palette preferences and lighting according to provided style.
If user provide multiple styles you need to combine it
It should be possible to edit this details in easy way
output should be plain text. ut should should be only prompt and nothing else, ensure there are no any comments, only prompt. I should just copy and use this prompt.
PROMPT to adopt:
{}
USE next styles: {}
Style description: {}. you need to adopt prompt to this style. change background, mood, atmosphere, colors, etc.
Style palette: {}
Next is user additional requirements that you should adopt it to prompt: {}
"""


def reformatIdeaPrompt(text_constant, *args):
    try:
        formatted_prompt_for_redesign = text_constant.format(*args)
        return formatted_prompt_for_redesign
    except KeyError as e:
        print(f"Error: Missing parameter '{e.args[0]}' in the text constant.")
        return None


@execution_time_decorator
def adopt_style(picture_prompt, style_name, additional_prompt=""):
    print(f"\tAdopting prompt to {style_name} ...")

    # read json from file styles.json
    file_with_styles = 'support/styles.json'
    with open(file_with_styles, 'r') as json_file:
        styles_map = json.load(json_file)
    try:
        style_description = styles_map[style_name]["description"]
        style_palette = styles_map[style_name]["palette"]
    except KeyError as e:
        print(f"Error: Somme issue with style '{style_name}'. \nCheck {file_with_styles} file.")
        exit(1)
        return None

    picture_prompt = reformatIdeaPrompt(init_prompt_for_reformating, picture_prompt, style_name, style_description, style_palette,additional_prompt)
    return picture_prompt

@execution_time_decorator
def get_dalle_prompt_based_on_input(OpenAIclient, input_prompt, model_to_chat):
    role = """As a Prompt Generator Specialist for DALL·E, you will craft detailed prompts that translate user ideas into vivid, DALL·E-compliant visual concepts, demanding creativity and an understanding of artistic styles. Your role involves refining prompts for accuracy, integrating various artistic elements, and ensuring they adhere to content guidelines. Collaboration with users to fine-tune their visions and enhance their experience with DALL·E is key. You'll analyze feedback from generated images to improve prompt effectiveness and educate users on creating impactful prompts. This position requires strong creative skills, language proficiency, and a good grasp of DALL·E's capabilities, offering a unique blend of art and technology."""
    print("\tGetting response from DALLE prompt generator ...")
    input_prompt = role + "\n here is user idea you need to improve and get ideal prompt" + input_prompt
    response_msg = get_prompt_result(OpenAIclient, input_prompt, role, model_to_chat)
    return response_msg


from typing import Any
import openai

def get_prompt_result(OpenAIclient: openai.Client, input_prompt: str, gpt_role: str, model_to_chat: str) -> Any:
    try:
        completion = OpenAIclient.chat.completions.create(
            model=model_to_chat,
            messages=[
                {"role": "assistant",
                 "content": input_prompt}
            ]
        )
    except Exception as e:
        print(f"Error during the request to OpenAI API: {e}")
        return None

    response_msg = completion.choices[0].message.content
    return response_msg


def generate_idea(prompt):
    # Implement idea generation logic
    return f"""
        Request for Detailed Prompt Creation for DALL-E 3 Illustration
        Idea Summary:
        {prompt}
        Request:
        I am seeking a comprehensive and detailed prompt to generate images using DALL-E 3. The prompt should be constructed with a high level of specificity, ensuring that each element of the idea is vividly described and easily understandable by DALL-E 3.
        Details must to Include in the Prompt:
        Setting: Describe the location or environment where the scene takes place, considering factors like time of day, weather, and specific setting characteristics.
        Characters: Detail any characters involved, including their appearance, attire, expressions, and actions. Mention the number of characters and their roles or significance in the scene.
        Objects and Props: List any significant objects or props that should be included, describing their appearance, placement, and relevance to the scene.
        Perspective and Composition: Indicate the desired perspective (e.g., first-person, bird's-eye) and composition elements (e.g., focus points, balance).
        Please ensure that the prompt is structured clearly, with each category distinctly defined. This structure should allow for easy modification of specific details, enabling me to adjust elements as needed while maintaining the overall integrity of the idea.

        requirements to answer:
        it should be only prompt. ensure there are no any other comments to the prompt. nor any comment in the beginning neither in the end.
        there should be separate section for each element of the idea. it should be clear what is setting, what is characters, what is objects and props, what is perspective and composition.
        there should be  clear separation where is main subject and where is details.
"""


def generate_multistyle_pictures(num_of_pictures, num_of_random_styles, list_of_styles):
    # Implement logic to generate pictures with multiple styles
    # Return a list of generated picture paths
    return []

def generate_picture_by_style(input_prompt, prompt_text, style):
    # Implement logic to generate a picture based on input prompt and style
    # Return the path to the generated picture
    return 'path_to_generated_picture.jpg'

def replace_last_path_part_with_datetime(file_path, style=""):
    # Split the file path into directory and file name parts
    directory, file_name = os.path.split(file_path)

    # Get the current date and time as a string
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the new file name with the current datetime
    new_file_name = f"{current_datetime}_{style}_{file_name}"

    # Combine the directory and new file name to form the new path
    new_file_path = os.path.join(directory, new_file_name)

    return new_file_path