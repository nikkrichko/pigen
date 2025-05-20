import click
from openai import OpenAI
from icecream import ic
import support.functions as sf
# Decorators used across CLI commands
from support.decorators import spinner_decorator, execution_time_decorator
# from support.functions import generate_image, save_picture, get_dalle_prompt_based_on_input, execution_time_decorator, save_text_to_file
import urllib3
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)
import concurrent.futures
import support.Configurator as Config
from support.logger import Logger, delog


openAIClient = OpenAI()


# model_to_chat = "gpt-3.5-turbo-1106"
# # model_to_chat = "gpt-4-1106-preview"
# model_to_image = "dall-e-3"
# # 1792x1024
# PIC_SIZE="1024x1024"
# # PIC_SIZE="1792x1024"
# PIC_QUALITY="hd"



# MAIN_MODEL: "gpt-3.5-turbo-0125"
# ART_MODEL: "dall-e-3"
# PIC_SIZE: "1024x1024"
# LOG_LEVEL: "INFO"
# PIC_QUALITY: "hd"



@click.group()
def cli():
    """CLI Application for Various Tasks"""
    pass

@delog()
@execution_time_decorator
@spinner_decorator
@cli.command()
@click.option('-p', '--prompt', default=None, help='Prompt text for generating an idea.')
@click.option('-i', '--inputfile', default=None, type=click.Path(exists=True), help='Input file with text for generating the idea.')
@click.option('-o', '--outputfile', required=True, type=click.Path(), help='Output file to save the generated idea.')
def idea(prompt, outputfile, inputfile):
    """
    Generate an Idea
    This method generates a prompt for generating pictures on a given prompt ideas. The generated idea is saved to an output file.
    Args:
        prompt (str): The prompt text for generating the idea.
        outputfile (str): The path of the output file to save the generated idea.
    Returns:
        None
    Example Usage:
        idea("--prompt 'give me a picture of a beautiful woman with handsome man.' --outputfile 'my_idea.txt'")
    """
    if prompt is None and inputfile is None:
        raise click.UsageError("You must provide either a prompt or an input file.")
    if prompt is not None and inputfile is not None:
        raise click.UsageError("You can't provide both a prompt and an input file.")

    if prompt is not None:
        text_prompt = prompt
    if inputfile is not None:
        with open(inputfile, 'r') as file:
            text_prompt = file.read().strip()

    print("\tGenerating prompt based on idea ...")

    result = sf.generate_and_save_idea(text_prompt, outputfile, openAIClient, model_to_chat)
    sf.log_prompt_output("idea", text_prompt, result)
    click.echo(f'Idea generated and saved to {outputfile}.')




@delog()
@execution_time_decorator
@spinner_decorator
@cli.command()
@click.option('-i', '--input_file', type=click.File('r'),  help='Input file with prompt text.')
@click.option('-s', '--style', type=str, help='List of styles to apply to the picture.[comma separated]')
@click.option('-r', '--random_num', type=int, default=0, help='Generate number of different random styles')
@click.option('-o', '--output_file', type=str, help='Where to save picture')
@click.option('-w', '--workers_num', type=int, default=3, help='Number of workers to use for parallel execution.')

def multistyle(input_file, style, output_file, workers_num, random_num):
    # Implement logic to generate pictures with specified styles
    if random_num != 0 and style is not None:
        raise Exception("You can't specify both random_num and list_of_styles. Please specify only one of them.")

    if random_num != 0:
        print(f"Generating num of random styles: {random_num}")
        list_of_styles = sf.get_random_styles_from_file(random_num)
    else:
        list_of_styles = style.split(",")

    print(f"List of styles: {list_of_styles}")

    # Define a function to perform task in parallel
    initial_idea_prompt = input_file.read()
    def task_gen_adopted_prompt(initial_idea_prompt, style,output_file):
        print(f"Processing style: {style}")
        additional_user_prompt = ""
        adopted_prompt = sf.generate_adopted_prompt(additional_user_prompt, initial_idea_prompt, style, openAIClient, model_to_chat)
        output_adopted_prompt_file = "temp/multi/03_adopted_prompt.txt"
        output_file_path = sf.replace_last_path_part_with_datetime(output_adopted_prompt_file, style)
        sf.save_text_to_file(adopted_prompt, output_file_path)
        image = sf.generate_image(adopted_prompt, openAIClient, size=PIC_SIZE, quality=PIC_QUALITY)
        if output_file:
            output_file = sf.replace_last_path_part_with_datetime(output_file, style)
        else:
            output_file = sf.default_output_file(style)
        sf.save_picture(output_file, image)
        sf.log_prompt_output("multistyle", adopted_prompt, output_file)

        return adopted_prompt

    # Use ThreadPoolExecutor to run the tasks in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers_num) as executor:
        executor.map(task_gen_adopted_prompt, [initial_idea_prompt]*len(list_of_styles), list_of_styles, [output_file]*len(list_of_styles))

    pass

@delog()
@execution_time_decorator
@spinner_decorator
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
    initial_idea_prompt = input_file.read()
    additional_user_prompt = prompt
    adopted_prompt = sf.generate_adopted_prompt(additional_user_prompt, initial_idea_prompt, style, openAIClient, model_to_chat)

    image = sf.generate_image(adopted_prompt, openAIClient, size=PIC_SIZE, quality=PIC_QUALITY)
    if output_file:
        output_file = sf.replace_last_path_part_with_datetime(output_file, style)
    else:
        output_file = sf.default_output_file(style)
    sf.save_picture(output_file, image)
    sf.log_prompt_output("picbystyle", adopted_prompt, output_file)
    click.echo(f'Picture generated with style "{style}" based on the input prompt and saved:\n---\n{output_file}')
    ic(f"Picture saved to {output_file}")


@delog()
@cli.command()
@click.option('-i', '--input_file', type=click.File('r'),  help='Input file with prompt text.')
@click.option('-o', '--output_file', type=str, help='Where to save picture')
def picFromPromptFile(input_file, output_file):
    initial_idea_prompt = input_file.read()
    image = sf.generate_image(initial_idea_prompt, openAIClient, size=PIC_SIZE, quality=PIC_QUALITY)
    if output_file:
        output_file = sf.replace_last_path_part_with_datetime(output_file, "")
    else:
        output_file = sf.default_output_file("")
    sf.save_picture(output_file, image)
    click.echo(f'Picture generated from file "{input_file}" based on the input prompt and saved:\n---\n{output_file}')
    ic(f"Picture saved to {output_file}")


@delog()
@cli.command()
@click.option('-n', '--name', required=True, help='Style title')
@click.option('-d', '--description', required=True, help='Style description')
@click.option('-p', '--palette', required=True, help='Color palette for the style')
def addstyle(name, description, palette):
    """Add a new style entry to the styles file."""
    try:
        sf.add_style_to_file(name, description, palette)
    except ValueError as exc:
        raise click.ClickException(str(exc))
    click.echo(f'Style "{name}" added to styles file.')


@delog()
@cli.command()
@click.option('-d', '--description', 'show_desc', is_flag=True,
              help='Display style descriptions.')
@click.option('-p', '--palette', 'show_palette', is_flag=True,
              help='Display palette information.')
def showstyles(show_desc, show_palette):
    """Print available styles."""
    styles = sf.load_styles()
    for name, info in styles.items():
        click.echo(f'Style: {name}')
        if show_desc:
            click.echo(f'  Description: {info.get("description", "")}')
        if show_palette:
            click.echo(f'  Palette: {info.get("palette", "")}')
        click.echo('')


@delog()
@execution_time_decorator
@spinner_decorator
@cli.command()
@click.option('-i', '--input_file', type=click.File('r', encoding="utf-8"), required=True,
              help='Input file containing the story text.')
@click.option('-o', '--output_file', type=str, required=True,
              help='Output JSON file to save the illustration data.')
@click.option('-n', '--num_scenes', type=int, default=10,
              help='Number of scenes to generate (default: 10).')
@click.option('-c', '--charfile', type=click.Path(exists=True, dir_okay=False),
              default=None,
              help='Optional JSON file with character descriptions.')
def ill_story(input_file, output_file, num_scenes, charfile):
    """
    Illustrate a story by generating character descriptions and scene breakdowns.

    This command analyzes a story text, extracts characters and their appearances,
    and generates detailed descriptions of key scenes for illustration purposes.
    The output is saved as a structured JSON file.

    Parameters:
    -----------
    input_file : file
        Input file containing the story text.
    output_file : str
        Path to save the output JSON file.
    num_scenes : int, optional
        Number of scenes to generate (default: 10).
    charfile : str, optional
        JSON file with pre-generated character descriptions. If provided,
        characters are loaded from this file instead of being generated.

    Returns:
    --------
    None

    Example usage:
    -------------
    pg.py ill_story --input_file story.txt --output_file illustration.json --num_scenes 12
    pg.py ill_story -i story.txt -o illustration.json -n 10 -c characters.json
    """
    # Read the story text from the input file
    story_text = input_file.read()
    # with open(input_file, "r", encoding="utf-8") as file:   # or "windows-1252", "latin-1", etc.
    #     story_text = file.read()


    # Log the command execution
    msg = f"Illustrating story from {input_file.name} with {num_scenes} scenes"
    if charfile:
        msg += f" using characters from {charfile}"
    msg += "..."
    click.echo(msg)

    # Ensure output file has .json extension
    if not output_file.lower().endswith('.json'):
        output_file += '.json'

    # Call the illustrate_story function
    result_file = sf.illustrate_story(
        story_text=story_text,
        output_file=output_file,
        num_scenes=num_scenes,
        openai_client=openAIClient,
        model=model_to_chat,
        charfile=charfile
    )

    # Check if the operation was successful
    if result_file:
        click.echo(f"Story illustration completed successfully!")
        click.echo(f"Output saved to: {result_file}")
        sf.log_prompt_output("ill_story", story_text[:500] + "..." if len(story_text) > 500 else story_text, result_file)
    else:
        click.echo("Failed to illustrate the story. Check the logs for details.")


if __name__ == '__main__':
    config = Config.Config()
    model_to_chat = config.get("MAIN_MODEL")
    model_to_image = config.get("ART_MODEL")
    PIC_SIZE = config.get("PIC_SIZE")
    PIC_QUALITY = config.get("PIC_QUALITY")
    cli()
