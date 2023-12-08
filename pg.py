import datetime
import os

import click
from openai import OpenAI
from icecream import ic
from support import functions as sf
# from support.functions import generate_image, save_picture, get_dalle_prompt_based_on_input, execution_time_decorator, save_text_to_file
import urllib3
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)
import support.functions as sf


openAIclient = OpenAI()
model_to_chat = "gpt-3.5-turbo-1106"
# model_to_chat = "gpt-4-1106-preview"
model_to_image = "dall-e-3"
# 1792x1024
PIC_SIZE="1024x1024"
PIC_SIZE="1792x1024"
PIC_QUALITY="hd"



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
    idea_text = sf.generate_idea(prompt)
    response_msg = sf.get_dalle_prompt_based_on_input(openAIclient, idea_text, model_to_chat)
    sf.save_text_to_file(response_msg, outputfile)
    click.echo(f'Idea generated and saved to {outputfile}.')




@cli.command()
@click.option('--numOfPictures', type=int, default=5, help='Number of pictures to generate.')
@click.option('--numOfRandomStyles', type=int, default=3, help='Number of random styles to apply.')
@click.option('--listofStyles', type=str, help='Comma-separated list of specific styles to apply.')
def multistyle(numofpictures, numofrandomstyles, listofstyles):
    # Implement logic to generate pictures with specified styles
    picture_paths = sf.generate_multistyle_pictures(numofpictures, numofrandomstyles, listofstyles)
    click.echo(f'{len(picture_paths)} pictures generated with multiple styles:')
    for path in picture_paths:
        click.echo(path)

@cli.command()
@click.option('-i', '--input_file', type=click.File('r'),  help='Input file with prompt text.')
@click.option('-p', '--prompt', type=str, help='Additional Prompt text for generating a picture.')
@click.option('-s', '--style', type=str, help='Style to apply to the picture.')
@click.option('-o', '--output_file', type=str, help='Where to save picture')
def picByStyle(input_file, prompt, style, output_file):
    """
    This method generates a picture based on a given style and prompt text.

    Parameters:
    - input_file: The input file that contains the prompt text. Should be opened in 'r' mode.
    - prompt: Additional prompt text to be used for generating the picture.
    - style: The style to apply to the picture.
    - output_file: The path where the generated picture will be saved. Should be a string.

    Returns:
    None

    Example usage:
    picByStyle(open('prompt.txt', 'r'), "Generate a beautiful landscape", "landscape_style", "output.png")
    """
    input_text = input_file.read()

    add_style = sf.adopt_style(input_text, style, prompt)
    sf.save_text_to_file(add_style, "temp/02_request_to_adopt_prompt.txt")

    print(f"\tAdopting initial prompt to style {style} ...")
    adopted_prompt = sf.get_dalle_prompt_based_on_input(openAIclient, add_style, model_to_chat)
    sf.save_text_to_file(adopted_prompt, "temp/03_adopted_prompt.txt")

    image = sf.generate_image(adopted_prompt, openAIclient, size=PIC_SIZE, quality=PIC_QUALITY)

    output_file = sf.replace_last_path_part_with_datetime(output_file, style)
    sf.save_picture(output_file, image)
    click.echo(f'Picture generated with style "{style}" based on the input prompt and saved:\n---\n{output_file}')
    ic(f"Picture saved to {output_file}")




if __name__ == '__main__':
    cli()