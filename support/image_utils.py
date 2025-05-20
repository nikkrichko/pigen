import base64
from typing import Any

import requests
import openai

from support.logger import Logger, delog
from support.decorators import spinner_decorator, execution_time_decorator

logger = Logger()


@delog()
@execution_time_decorator
@spinner_decorator
def generate_image(picture_prompt: str, openai_client: openai.Client, model: str = "gpt-image-1", size: str = "1024x1024", quality: str = "standard", num_of_pics: int = 1) -> bytes:
    """Generate an image using the OpenAI API and return it as bytes."""
    logger.log("\tGenerating image ...")
    img = openai_client.images.generate(
        model=model,
        prompt=picture_prompt,
        n=num_of_pics,
        size=size,
    )

    first = img.data[0]
    if hasattr(first, "b64_json"):
        return base64.b64decode(first.b64_json)
    url = first.url
    response = requests.get(url)
    return response.content


def save_picture(file_name: str, picture: bytes) -> None:
    """Write image bytes to ``file_name``."""
    logger.log("\t\tsaving image ...")
    with open(file_name, "wb") as fh:
        fh.write(picture)
    logger.log(f"\t\tImage saved to {file_name}.")
