import datetime
import os
from typing import Any

from support.logger import Logger

TEMP_DIR = "temp"

logger = Logger()


def save_text_to_file(text: str, filename: str) -> None:
    """Save ``text`` to ``filename`` using UTF-8 encoding."""
    logger.log("\t\tSaving text ...")
    with open(filename, "w", encoding="utf-8", errors="replace") as fh:
        fh.write(text)
    logger.log(f"\t\tText saved to {filename}.")


def replace_last_path_part_with_datetime(file_path: str, style: str = "") -> str:
    """Return ``file_path`` with the filename replaced by a timestamp."""
    directory, file_name = os.path.split(file_path)
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name = f"{current_datetime}_{style}_{file_name}"
    return os.path.join(directory, new_file_name)


def default_output_file(style: str, extension: str = ".png") -> str:
    """Return a path inside ``TEMP_DIR`` with timestamp and style."""
    os.makedirs(TEMP_DIR, exist_ok=True)
    current_datetime = datetime.datetime.now().strftime("%d%m%y_%H%M%S")
    style_part = f"_{style}" if style else ""
    file_name = f"{current_datetime}{style_part}{extension}"
    return os.path.join(TEMP_DIR, file_name)


def log_prompt_output(command_name: str, prompt_text: str, output_text: str) -> str:
    """Log a prompt and its output to a YAML file and return the path."""
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
