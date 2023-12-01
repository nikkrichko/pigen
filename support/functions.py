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
    # downloads the image to a file
    bin_picture = requests.get(image_url)
    return bin_picture.content

def save_picture(file_name, picture):
    print("\t\tsaving image ...")
    file = open(file_name, "wb")
    file.write(picture)
    file.close()



init_prompt_for_reformating = """
rephase next basic idea prompt with adding style details.
think about it at this prompt at first. it should pass all next criterias:
ensure that output prompt should be less than 2500 char wiouth loosing main idea and critterias.
ensure that the output prompt adheres to DALL-E 3's policy limitations while preserving the main idea and criteria. 
Add as much details as possible. 
Provide a comprehensive description for the main subject of the picture, including intricate details of their appearance, pose, expression, attire, and any relevant surroundings or props. The goal is to create a vivid and immersive visual description that leaves no aspect of the subject to the imagination.
Add background description according to the style. but background should contain also a lot of details but it should not distract from the main subject of the picture or illustration
man subject should beon 3/4 of the picture
you need also to describe Mood and Atmosphere: Convey the overall mood or atmosphere of the illustration, including color palette preferences and lighting according to provided style.
If user provide multiple styles you need to combine it
It should be possible to edit this details in easy way
output should be plain text. ut should should be only prompt and nothing else, ensure there are no any comments, only prompt. I should just copy and use this prompt.
PROMPT to adopt:
{}
USE next styles: {}
Style description: {}. you need to adopt prompt to this style. change background, mood, atmosphere, colors, etc.
Style palette: {}
"""
def reformatedIdeaPrompt(text_constant, *args):
    try:
        formatted_prompt_for_redesign = text_constant.format(*args)
        return formatted_prompt_for_redesign
    except KeyError as e:
        print(f"Error: Missing parameter '{e.args[0]}' in the text constant.")
        return None


@execution_time_decorator
def adopt_style(picture_prompt, style_name):
    # read json from file styles.json
    print(f"\tAdopting prompt to {style_name} ...")
    with open('support/styles.json', 'r') as json_file:
        # Load the JSON data into a Python dictionary
        styles_map = json.load(json_file)
    style_description = styles_map[style_name]["description"]
    style_palette = styles_map[style_name]["palette"]
    # add cartoon_style and cartoon_palette to prompt
    picture_prompt = reformatedIdeaPrompt(init_prompt_for_reformating,picture_prompt, style_name, style_description, style_palette)
    return picture_prompt

def get_dalle_prompt_based_on_input(OpenAIclient, input_prompt, model_to_chat):
    role = """As a Prompt Generator Specialist for DALL·E, you will craft detailed prompts that translate user ideas into vivid, DALL·E-compliant visual concepts, demanding creativity and an understanding of artistic styles. Your role involves refining prompts for accuracy, integrating various artistic elements, and ensuring they adhere to content guidelines. Collaboration with users to fine-tune their visions and enhance their experience with DALL·E is key. You'll analyze feedback from generated images to improve prompt effectiveness and educate users on creating impactful prompts. This position requires strong creative skills, language proficiency, and a good grasp of DALL·E's capabilities, offering a unique blend of art and technology."""

    completion = OpenAIclient.chat.completions.create(
        model=model_to_chat,
        messages=[
            {"role": "system",
             "content": role},
            {"role": "user",
             "content": input_prompt}
        ]
    )
    response_msg = completion.choices[0].message.content
    return response_msg


