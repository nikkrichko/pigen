import click

from openai import OpenAI
client = OpenAI()
model_to_chat = "gpt-3.5-turbo-1106"


@click.group()
def cli():
    """CLI Application for Various Tasks"""
    pass

@cli.command()
@click.option('--prompt', required=True, help='Prompt text for generating an idea.')
@click.option('--outputfile', required=True, type=click.Path(), help='Output file to save the generated idea.')
def idea(prompt, outputfile):
    """Generate an idea based on a prompt and save it to a file."""
    # Implement the logic to generate an idea based on the provided prompt
    idea_text = generate_idea(prompt)

    role = """As a Prompt Generator Specialist for DALL·E, you will craft detailed prompts that translate user ideas into vivid, DALL·E-compliant visual concepts, demanding creativity and an understanding of artistic styles. Your role involves refining prompts for accuracy, integrating various artistic elements, and ensuring they adhere to content guidelines. Collaboration with users to fine-tune their visions and enhance their experience with DALL·E is key. You'll analyze feedback from generated images to improve prompt effectiveness and educate users on creating impactful prompts. This position requires strong creative skills, language proficiency, and a good grasp of DALL·E's capabilities, offering a unique blend of art and technology."""

    final_prompt_for_idea = f"""
        Request for Detailed Prompt Creation for DALL-E 3 Illustration
        Idea Summary:
        {idea_text}
        Request:
        I am seeking a comprehensive and detailed prompt to generate images using DALL-E 3. The prompt should be constructed with a high level of specificity, ensuring that each element of the idea is vividly described and easily understandable by DALL-E 3.
        Details must to Include in the Prompt:
        Setting: Describe the location or environment where the scene takes place, considering factors like time of day, weather, and specific setting characteristics.
        Characters: Detail any characters involved, including their appearance, attire, expressions, and actions. Mention the number of characters and their roles or significance in the scene.
        Objects and Props: List any significant objects or props that should be included, describing their appearance, placement, and relevance to the scene.
        Perspective and Composition: Indicate the desired perspective (e.g., first-person, bird's-eye) and composition elements (e.g., focus points, balance).
        Please ensure that the prompt is structured clearly, with each category distinctly defined. This structure should allow for easy modification of specific details, enabling me to adjust elements as needed while maintaining the overall integrity of the idea.
        
        requirements to answer:
        it should be only prompt. ensure there are no any other comments to the prompt
"""

    completion = client.chat.completions.create(
        model=model_to_chat,
        messages=[
            {"role": "system",
             "content": role},
            {"role": "user",
             "content": final_prompt_for_idea}
        ]
    )
    response_msg = completion.choices[0].message.content
    # print(response_msg)

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
@click.argument('input_prompt', type=click.File('r'))
@click.argument('prompt_text', type=str)
@click.argument('style', type=str)
def picByStyle(input_prompt, prompt_text, style):
    """Generate a picture based on an input prompt and a style."""
    # Read the input prompt file and get its content
    input_text = input_prompt.read()

    # Implement logic to generate a picture based on the input prompt and style
    picture_path = generate_picture_by_style(input_text, prompt_text, style)
    click.echo(f'Picture generated with style "{style}" based on the input prompt: {picture_path}')

# Replace the placeholder functions with your actual logic
def generate_idea(prompt):
    # Implement idea generation logic
    return f'Idea generated based on prompt: "{prompt}"'

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