# pigen

## TL;DR
Generate image prompts and pictures with OpenAI's DALL·E API using a simple
command-line tool.

Utilities for generating images with OpenAI's DALL·E API. The project provides a
CLI (`pg.py`) that helps you craft prompts and render pictures in various
styles.

## Installation

1. Clone the repository and enter its folder:
   ```bash
   git clone <repo-url>
   cd pigen
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your `OPENAI_API_KEY` environment variable. In a Unix shell use
   `export OPENAI_API_KEY=<your-key>`.

## Quick Usage

The CLI supports several commands for working with prompts and pictures. A few
examples:

- Generate an idea prompt and save it to a file
  ```bash
  python pg.py idea --prompt "Generate a new project idea" --outputfile idea.txt
  ```
- Create multiple images using predefined styles
  ```bash
  python pg.py multistyle -i idea.txt -s "style1,style2" --output_file out.png
  ```
- Generate a picture in a single style
  ```bash
  python pg.py picbystyle -i idea.txt -p "extra details" -s style1 --output_file result.png
  ```

In short, the pipeline is:

1. Generate an idea text with `pg.py idea`.
2. Apply one or more styles using `picbystyle` or `multistyle`.
3. The final prompt is sent to DALL·E and the image is saved with a timestamp.

More detailed instructions, including configuration and available styles, can be
found in [docs/CREATING_PICTURES.md](docs/CREATING_PICTURES.md).
