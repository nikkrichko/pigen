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
- Add a new style to the styles file
  ```bash
  python pg.py addstyle -n test -d "this is a test style description" -p "orange, blue"
  ```
- Show available styles
  ```bash
  python pg.py showstyles
  ```
- Illustrate a story by generating character descriptions and scene breakdowns
  ```bash
  python pg.py ill-story -i story.txt -o illustration.json -n 10
  # reuse existing characters
  python pg.py ill-story -i story.txt -o illustration.json -n 10 -c chars.json
  ```


If you omit ``--output_file`` the image is saved inside ``temp/`` with a
timestamped name like ``010124_120000_style1.png``.

In short, the pipeline is:

1. Generate an idea text with `pg.py idea`.
2. Apply one or more styles using `picbystyle` or `multistyle`.
3. The final prompt is sent to DALL·E and the image is saved with a timestamp.

More detailed instructions can be found in:
- [Creating Pictures](docs/CREATING_PICTURES.md) - How to generate images with styles
- [Illustrating Stories](docs/ILLUSTRATING_STORIES.md) - How to analyze stories for illustration

## Configuration

Runtime options are stored in `config.yaml`. Key settings include:

- `MAIN_MODEL` – ChatGPT model used for prompt generation. Switch this to a GPT‑4 model if your
  account allows it.
- `ART_MODEL` – DALL·E version for images (currently `dall-e-3`).
- `PIC_SIZE` – Desired output size such as `1024x1024` or `1792x1024`.
- `PIC_QUALITY` – Set to `Standard` or `hd` for higher fidelity pictures.
- `LOG_LEVEL` – Console log verbosity.

Adjust these values to fit your workflow and API quota.

## Extending `styles.json`

The file `support/styles.json` holds all available art styles. Use `pg.py addstyle` to add one
interactively or edit the JSON manually. A minimal entry looks like:

```json
{
  "Comic_Book": {
    "description": "Bold ink lines with halftone shading.",
    "palette": "Strong primaries with black and white"
  }
}
```

After saving you can reference the new style with `-s Comic_Book`.

## Tests

Mock-based tests covering each pipeline step live in the `tests/` folder. See
[docs/tests/USAGE.md](docs/tests/USAGE.md) for instructions on running them.
The `test_addstyle.py` module ensures the `addstyle` command works as expected
and demonstrates how to add and remove a sample style entry.
