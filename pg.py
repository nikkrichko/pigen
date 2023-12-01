import click
from openai import OpenAI
from icecream import ic
from support import functions as sf
from support.functions import generate_image, save_picture, get_dalle_prompt_based_on_input, execution_time_decorator
import urllib3
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)

openAIclient = OpenAI()
model_to_chat = "gpt-3.5-turbo-1106"
# model_to_chat = "gpt-4"
# model_to_image = "dall-e-3"
PIC_SIZE="1024x1024"
PIC_QUALITY="standard"



@click.group()
def cli():
    """CLI Application for Various Tasks"""
    pass

@cli.command()
@click.option('--prompt', required=True, help='Prompt text for generating an idea.')
@click.option('--outputfile', required=True, type=click.Path(), help='Output file to save the generated idea.')
def idea(prompt, outputfile):
    """Generate an idea based on a prompt and save it to a file."""
    print("\tGenerating prompt based on idea ...")
    # Implement the logic to generate an idea based on the provided prompt
    idea_text = generate_idea(prompt)


#     final_prompt_for_idea = f"""
#         Request for Detailed Prompt Creation for DALL-E 3 Illustration
#         Idea Summary:
#         {idea_text}
#         Request:
#         I am seeking a comprehensive and detailed prompt to generate images using DALL-E 3. The prompt should be constructed with a high level of specificity, ensuring that each element of the idea is vividly described and easily understandable by DALL-E 3.
#         Details must to Include in the Prompt:
#         Setting: Describe the location or environment where the scene takes place, considering factors like time of day, weather, and specific setting characteristics.
#         Characters: Detail any characters involved, including their appearance, attire, expressions, and actions. Mention the number of characters and their roles or significance in the scene.
#         Objects and Props: List any significant objects or props that should be included, describing their appearance, placement, and relevance to the scene.
#         Perspective and Composition: Indicate the desired perspective (e.g., first-person, bird's-eye) and composition elements (e.g., focus points, balance).
#         Please ensure that the prompt is structured clearly, with each category distinctly defined. This structure should allow for easy modification of specific details, enabling me to adjust elements as needed while maintaining the overall integrity of the idea.
#
#         requirements to answer:
#         it should be only prompt. ensure there are no any other comments to the prompt. nor any comment in the beginning neither in the end.
# """

    response_msg = get_dalle_prompt_based_on_input(openAIclient, idea_text, model_to_chat)

    # Save the generated idea to the output file
    save_to_file(response_msg, outputfile)
    click.echo(f'Idea generated and saved to {outputfile}.')




@cli.command()
@click.option('--numOfPictures', type=int, default=5, help='Number of pictures to generate.')
@click.option('--numOfRandomStyles', type=int, default=3, help='Number of random styles to apply.')
@click.option('--listofStyles', type=str, help='Comma-separated list of specific styles to apply.')
def multistyle(numofpictures, numofrandomstyles, listofstyles):
    """Generate pictures with multiple styles."""
    # Implement logic to generate pictures with specified styles
    picture_paths = generate_multistyle_pictures(numofpictures, numofrandomstyles, listofstyles)
    click.echo(f'{len(picture_paths)} pictures generated with multiple styles:')
    for path in picture_paths:
        click.echo(path)

@cli.command()
@click.option('-i', '--input_file', type=click.File('r'),  help='Input file with prompt text.')
@click.option('-p', '--prompt', type=str, help='Additional Prompt text for generating a picture.')
@click.option('-s', '--style', type=str, help='Style to apply to the picture.')
@click.option('-o', '--output_file', type=str, help='Where to save picture')
def picByStyle(input_file, prompt, style, output_file):
    """Generate a picture based on an input prompt and a style."""
    # Read the input prompt file and get its content
    input_text = input_file.read()

    add_style = sf.adopt_style(input_text, style)
    save_to_file(add_style, "temp/02_request_to_adopt_prompt.txt")
    # ic(add_style)
    adopted_prompt = sf.get_dalle_prompt_based_on_input(openAIclient, add_style, model_to_chat)
    save_to_file(adopted_prompt, "temp/03_adopted_prompt.txt")
    # ic(adopted_prompt)
    # Implement logic to generate a picture based on the input prompt and style
    # picture_path = generate_picture_by_style(input_text, adopted_prompt, style)
    # click.echo(f'Picture generated with style "{style}" based on the input prompt: {picture_path}')
    image = generate_image(adopted_prompt, openAIclient)
    output_file = output_file.replace("/", f"/{style}_")
    save_picture(output_file, image)
    ic(f"Picture saved to {output_file}")
    ic("Done!")

# Replace the placeholder functions with your actual logic
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

def save_to_file(text, filename):
    # Implement logic to save text to a file
    with open(filename, 'w') as file:
        file.write(text)

def generate_multistyle_pictures(num_of_pictures, num_of_random_styles, list_of_styles):
    # Implement logic to generate pictures with multiple styles
    # Return a list of generated picture paths
    return []

def generate_picture_by_style(input_prompt, prompt_text, style):
    # Implement logic to generate a picture based on input prompt and style
    # Return the path to the generated picture
    return 'path_to_generated_picture.jpg'

if __name__ == '__main__':
    cli()