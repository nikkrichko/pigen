"""Utility script for generating images with DALL·E."""

import datetime
import json
import os
from pprint import pprint as pp

import requests
from openai import OpenAI
from typing import Optional


CLIENT = OpenAI()

# Default settings
FOLDER_NAME = "examples"
FILE_NAME = "diff_styles"
STYLE_NAME = "Cartoon_Realism"
AMOUNT_OF_PICTURES = 1


def generate_image(picture_prompt: str) -> bytes:
    """Generate an image from ``picture_prompt`` using OpenAI."""
    print("\tGenerating image ...")
    response = CLIENT.images.generate(
        model="dall-e-3",
        prompt=picture_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    bin_picture = requests.get(image_url)
    return bin_picture.content


def save_picture(file_name: str, picture: bytes) -> None:
    """Save ``picture`` to ``file_name``."""
    print("\t\tsaving image ...")
    with open(file_name, "wb") as fh:
        fh.write(picture)




# if not os.path.exists(file_name):
#     os.mkdir(file_name)

def load_prompt(path: str = "prompt.txt") -> str:
    """Load the base prompt from ``path``."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def load_styles(path: str = "styles.json") -> dict:
    """Load available styles from ``path``."""
    with open(path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


STYLES_MAP = load_styles()


def style_prompt(prompt: str, style_name: str) -> str:
    """Append style information to ``prompt``."""
    style_description = STYLES_MAP[style_name]["description"]
    style_palette = STYLES_MAP[style_name]["palette"]
    return f"{prompt}\nstyle:{style_description}\ncolors:{style_palette}"



def gen_variants(picture_prompt: str, file_name: str, folder_name: str, num_of_pictures: int = 1) -> None:
    """Generate images for all styles found in ``STYLES_MAP``."""
    for name, info in STYLES_MAP.items():
        print("Style Name:", name)
        styled_prompt = style_prompt(picture_prompt, name)
        for item in range(1, num_of_pictures + 1):
            print("Iteration", item, "of", name, "style")
            try:
                style_name_collapsed = name.replace(" ", "_")
                collapsed_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                file_name_with_path = os.path.join(
                    folder_name,
                    file_name,
                    f"{style_name_collapsed}_{file_name}_{collapsed_time}.png",
                )
                picture = generate_image(styled_prompt)
                save_picture(file_name_with_path, picture)
            except Exception as exc:  # pragma: no cover - basic example
                pp(f"style:{name} \nAn error occurred for item {item}: {exc}")
                continue

def generate_pic_in_style(
    num_of_pictures: int,
    picture_prompt: str,
    file_name: str,
    folder_name: str,
    style_name: Optional[str] = None,
) -> None:
    """Generate ``num_of_pictures`` in a specific ``style_name``."""
    collapsed_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if style_name is not None:
        picture_prompt = style_prompt(picture_prompt, style_name)
        style_name_collapsed = style_name.replace(" ", "_")
        file_name_with_path = os.path.join(
            folder_name, f"{style_name_collapsed}_{file_name}_{collapsed_time}.png"
        )
    else:
        file_name_with_path = os.path.join(
            folder_name, f"{file_name}_{collapsed_time}.png"
        )

    for i in range(1, num_of_pictures + 1):
        print("Iteration", i, "/", num_of_pictures)
        picture = generate_image(picture_prompt)
        save_picture(file_name_with_path, picture)



####  prin datetime to know when it starts

# measure timeof execution
def main() -> None:
    """Entry point for the script."""
    folder = os.path.join(FOLDER_NAME, FILE_NAME)
    os.makedirs(folder, exist_ok=True)

    prompt = load_prompt()
    prompt = style_prompt(prompt, STYLE_NAME)

    generate_pic_in_style(
        AMOUNT_OF_PICTURES,
        prompt,
        FILE_NAME,
        folder,
        style_name=None,
    )


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print("Start execution iteration at >>>>>>>>>>>>>>>>>", start_time)
    main()
    finish_time = datetime.datetime.now()
    print("Start time: ", start_time)
    print("Finish time: ", finish_time)
    print("Total time: ", finish_time - start_time)
    print("Done! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
