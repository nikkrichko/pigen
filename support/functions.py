import random
from typing import Any
import openai
import json
import os
import requests
import datetime
import sys
from support.decorators import spinner_decorator, execution_time_decorator
from support.logger import delog
import base64

ADOPT_PROMPT_TXT_PATH = "temp/02_request_to_adopt_prompt.txt"
ADOPTED_PROMPT_PATH = "temp/03_adopted_prompt.txt"
FILE_WITH_STYLES = 'support/styles.json'
TEMP_DIR = "temp"


# Define the decorator

@execution_time_decorator
@spinner_decorator
def generate_image(picture_prompt, openai_client, model="gpt-image-1", size="1024x1024", quality="standard", num_of_pics=1):
    global response
    print("\tGenerating image ...")
    # response = openai_client.images.generate(
    #     model=model,
    #     prompt=picture_prompt,
    #     size=size,
    #     quality=quality,
    #     n=num_of_pics,
    # )
    # image_url = response.data[0].url
    # bin_picture = requests.get(image_url)
    img = openai_client.images.generate(
        model=model,
        prompt=picture_prompt,
        n=num_of_pics,
        size=size
    )

    image_bytes = base64.b64decode(img.data[0].b64_json)

    return image_bytes

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
output should be plain text. It should be only prompt and nothing else, ensure there are no any comments, only prompt. I should just copy and use this prompt.
PROMPT to adopt:
{}
USE next styles: {}
Style description: {}. you need to adopt prompt to this style. change background, mood, atmosphere, colors, etc.
Style palette: {}
Next is user additional requirements that you should adopt it to prompt: {}

Ensure that the output prompt should be less than 2500 char without loosing main idea and criteria.
"""


@spinner_decorator
def reformatIdeaPrompt(text_constant, *args):
    try:
        formatted_prompt_for_redesign = text_constant.format(*args)
        return formatted_prompt_for_redesign
    except KeyError as e:
        print(f"Error: Missing parameter '{e.args[0]}' in the text constant.")
        return None


def get_random_styles_from_file( num_of_styles):
    with open(FILE_WITH_STYLES, 'r') as json_file:
        styles_map = json.load(json_file)
    styles = list(styles_map.keys())
    random_styles = random.sample(styles, num_of_styles)
    return random_styles


@execution_time_decorator
def adopt_style(picture_prompt, style_name, additional_prompt=""):
    print(f"\tAdopting prompt to {style_name} ...")
    # read json from file styles.json

    # TODO if style_name is not in styles.json then resuest for style description and palette at chatgpt

    with open(FILE_WITH_STYLES, 'r') as json_file:
        styles_map = json.load(json_file)
    try:
        style_description = styles_map[style_name]["description"]
        style_palette = styles_map[style_name]["palette"]
    except KeyError as e:
        print(f"Error: Somme issue with style '{style_name}'. \nCheck {FILE_WITH_STYLES} file.")
        exit(1)
        return None

    picture_prompt = reformatIdeaPrompt(init_prompt_for_reformating, picture_prompt, style_name, style_description, style_palette,additional_prompt)
    return picture_prompt

def generate_adopted_prompt(additional_user_prompt, initial_idea_prompt, style,openAIClient,model_to_chat):
    add_style = adopt_style(initial_idea_prompt, style, additional_user_prompt)
    save_text_to_file(add_style, ADOPT_PROMPT_TXT_PATH)
    print(f"\tAdopting initial prompt to style {style} ...")
    adopted_prompt = get_dalle_prompt_based_on_input(openAIClient, add_style, model_to_chat)
    save_text_to_file(adopted_prompt, ADOPTED_PROMPT_PATH)
    return adopted_prompt

@execution_time_decorator
def get_dalle_prompt_based_on_input(OpenAIclient, input_prompt, model_to_chat):
    role = """As a Prompt Generator Specialist for DALL·E, you will craft detailed prompts that translate user ideas into vivid, DALL·E-compliant visual concepts, demanding creativity and an understanding of artistic styles. Your role involves refining prompts for accuracy, integrating various artistic elements, and ensuring they adhere to content guidelines. Collaboration with users to fine-tune their visions and enhance their experience with DALL·E is key. You'll analyze feedback from generated images to improve prompt effectiveness and educate users on creating impactful prompts. This position requires strong creative skills, language proficiency, and a good grasp of DALL·E's capabilities, offering a unique blend of art and technology."""
    print("\tGetting response from DALLE prompt generator ...")
    input_prompt = role + "\n here is user idea you need to improve and get ideal prompt" + input_prompt
    response_msg = get_prompt_result(OpenAIclient, input_prompt, role, model_to_chat)
    return response_msg




def get_prompt_result(OpenAIclient: openai.Client, input_prompt: str, gpt_role: str, model_to_chat: str) -> Any:
    try:
        completion = OpenAIclient.chat.completions.create(
            model=model_to_chat,
            messages=[
                {"role": "assistant", "content": input_prompt}
            ]
        )
    except getattr(openai, "APIConnectionError", Exception) as e:
        print(f"Connection error when communicating with OpenAI: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during the request to OpenAI API: {e}")
        sys.exit(1)

    response_msg = completion.choices[0].message.content
    return response_msg

@spinner_decorator
@delog()
def generate_and_save_idea(prompt, outputfile, openAIclient, model_to_chat):
    idea_text = generate_idea(prompt)
    response_msg = get_prompt_result(openAIclient, idea_text, model_to_chat=model_to_chat, gpt_role ="")
    save_text_to_file(response_msg, outputfile)
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
        Please ensure that the prompt is structured clearly, with each category distinctly defined. 
        This structure should allow for easy modification of specific details, enabling me to adjust elements as needed while maintaining the overall integrity of the idea.
        Identify as much main subject as possible. Ensure that the main subject is clearly separated from the background and other details.
        Each main elements hshold have own sections and onw categories of description.
        Each element of the resulted prompt should have own category and it should be easy to modify it. Split prompt to sections, as much as possible sections. 
        Each category and sub category should easy to separete and modify. Better more categories with less details than less categories with more details.
        

        requirements to answer:
        It should be only prompt. Ensure there are no any other comments to the prompt. nor any comment in the beginning neither in the end.
        there should be separate section for each element of the idea. it should be clear what is setting, what is characters, what is objects and props, what is perspective and composition.
        there should be  clear separation where is main subject and where is details.
        answer should be in yaml. but it should not contain any  quoutes n the beginning or in the end. Just text like a yaml.
        use next structure of like an example, but not limit yourself if it requires to create more comprehensive prompt.
        Scene Description:
  - Setting:
    - Location
    - Time of Day
    - Weather
	- Geography
  - Characters:
    - Number of Characters
    - Character Appearances
    - Character Actions
	- Character Relationships
  - Objects and Props:
    - Main Subject
    - Relevant Objects
    - Props
    - Environmental Elements
	- Other Objects
	
  - Perspective and Composition:
    - Viewing Angle
    - Composition Style
    - Focal Point
    - Balance and Symmetry
    - Depth of Field
  - Action and Movement:
    - Primary Action
    - Secondary Actions
    - Character Movement
  - Lighting and Shadows:
    - Lighting Sources
	- Lighting Style
    - Shadows
  - Color Palette:
    - Dominant Colors
    - Color Contrast
  - Mood and Atmosphere:
    - Emotional Tone
    - Atmosphere
    - Tension Level
    - Overall Mood
  - Architecture and Design:
    - Architectural Style
    - Design Details
	- Building Materials
    - Structural Details
    - Interior Design
  - Seasons:
    - Seasonal Setting
    - Seasonal Changes
    - Seasonal Activities
    - Natural Phenomena
  - Nature Elements:
    - Flora
    - Fauna
	- Landscape Features
    - Vegetation
    - Natural Elements
    - Bodies of Water
    - Terrain Characteristics
  - Animals and Wildlife:
    - Animal Species
    - Animal Behavior
    - Habitat Details
    - Wildlife Interactions
  - Industrial Environments:
    - Factories and Mills
    - Machinery and Manufacturing
    - Urban Industrial Scenes
    - Pollution and Smoke
  - Cultural Landscapes:
    - Cultural Heritage Sites
    - Historical Monuments
    - Cultural Significance
    - Traditional Architecture
  - Vehicles and Transportation:
    - Types of Vehicles
    - Vehicle Placement
	- Vehicle Condition
    - Traffic
    - Transportation Infrastructure
  - Technology and Gadgets:
    - Technological Features
    - High-Tech Devices
  - Clothing and Attire:
    - Clothing Styles
    - Accessories
    - Costume Details
    - Fashion Era
  - Interiors:
    - Furniture and Decor
	- Interior Design Themes
    - Furniture Styles
    - Decorative Details
    - Room Layout

  - History and Era:
    - Historical Period
    - Era-specific Details
	- Historical Era
    - Notable Historical Figures
    - Historical Artifacts
	- Anachronisms
  - Symbolism and Iconography:
    - Symbols
    - Iconic Imagery
  - Transportation:
    - Modes of Transportation
    - Transportation Infrastructure
  - Cuisine and Food:
    - Types of Food
    - Food Presentation
    - Dining Setup
    - Culinary Details
  - Events and Festivals:
    - Event Type
    - Crowd Size
    - Performances
    - Decorations
  - Crowd and Activities:
    - Size of the Crowd
    - Activities and Interactions
        
        
        
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


def add_style_to_file(name: str, description: str, palette: str, file_path: str = FILE_WITH_STYLES) -> None:
    """Add a new style entry to the styles file.

    Parameters
    ----------
    name: str
        Name of the style to add.
    description: str
        Text description of the style.
    palette: str
        Color palette description for the style.
    file_path: str, optional
        Path to the JSON file storing styles.
    """
    with open(file_path, "r", encoding="utf-8") as fh:
        styles = json.load(fh)

    if name in styles:
        raise ValueError(f"Style '{name}' already exists.")

    styles[name] = {"description": description, "palette": palette}

    with open(file_path, "w", encoding="utf-8") as fh:
        json.dump(styles, fh, indent=4, ensure_ascii=False)


def load_styles(file_path: str = FILE_WITH_STYLES) -> dict:
    """Return all styles from ``file_path`` as a dictionary."""
    with open(file_path, "r", encoding="utf-8") as fh:
        return json.load(fh)

        
    
def default_output_file(style: str, extension: str = ".png") -> str:
    """Return a default output file path for a generated image.

    The path points inside ``TEMP_DIR`` which will be created if it does not
    exist. The filename is composed from the current date/time and the style
    name using the ``ddmmyy_HHMMSS`` format, e.g. ``010124_120000_Anime.png``.

    Parameters
    ----------
    style: str
        Style name to include in the filename.
    extension: str, optional
        File extension (including the leading dot). ``.png`` by default.

    Returns
    -------
    str
        Full path to the default output file.
    """

    os.makedirs(TEMP_DIR, exist_ok=True)
    current_datetime = datetime.datetime.now().strftime("%d%m%y_%H%M%S")
    style_part = f"_{style}" if style else ""
    file_name = f"{current_datetime}{style_part}{extension}"
    return os.path.join(TEMP_DIR, file_name)


def log_prompt_output(command_name: str, prompt_text: str, output_text: str) -> str:
    """Log a prompt and its output to a YAML file.

    Parameters
    ----------
    command_name: str
        Name of the CLI command being executed.
    prompt_text: str
        Prompt text that was provided to the command.
    output_text: str
        The textual result or output file path produced by the command.

    Returns
    -------
    str
        Path to the created YAML log file.
    """

    now = datetime.datetime.now()
    date_part = now.strftime("%d%m%y")
    time_part = now.strftime("%H%M%S")
    base_dir = os.path.join("log", command_name, date_part)
    os.makedirs(base_dir, exist_ok=True)
    log_file = os.path.join(base_dir, f"{date_part}_{time_part}_{command_name}.yaml")

    prompt_block = str(prompt_text).replace("\n", "\n  ")
    output_block = str(output_text).replace("\n", "\n  ")
    content = f"prompt: |\n  {prompt_block}\noutput: |\n  {output_block}\n"
    with open(log_file, "w", encoding="utf-8") as fh:
        fh.write(content)

    return log_file



