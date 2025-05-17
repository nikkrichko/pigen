# Creating Pictures with `pigen`

This guide explains how to use the command line interface provided by the
`pigen` project to generate images with different styles using OpenAI's
API. It assumes you already have Python 3 installed and an OpenAI API key.

## Pipeline Overview

The tool follows a simple pipeline to transform your idea into a finished
picture. Understanding each stage will help you customize the results:

1. **Idea Generation** – Using the `idea` command, a short concept is
   expanded into a detailed description. The helper function
   `generate_and_save_idea` (defined in `support/functions.py`) sends your
   prompt to ChatGPT and saves the response to a file.
2. **Prompt Adoption** – Commands such as `picbystyle` and `multistyle`
   read the idea file and adapt it to a specific style. The
   `generate_adopted_prompt` function merges the idea with a style
   description and palette from `support/styles.json` to build a DALL·E
   compliant prompt.
3. **Image Generation** – The adopted prompt is passed to DALL·E through
   `generate_image`. This function requests the final image and the result
   is written to disk via `save_picture`.
4. **Review Outputs** – Intermediate prompts are stored in the `temp`
   directory. Generated images receive timestamps so you can easily track
   different versions.

The next sections walk through the commands that orchestrate these steps.

## Installation

1. Clone the repository and change into its directory:
   ```bash
   git clone <repo-url>
   cd pigen
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the environment variable `OPENAI_API_KEY` with your API key. For
   example:
   ```bash
   export OPENAI_API_KEY=<your-key>
   ```
   On Windows use `set` inside a Command Prompt or `$env:OPENAI_API_KEY` in
   PowerShell.

## Basic Workflow

1. **Generate an Idea Prompt** (optional)

   The `idea` command can create a detailed picture description that can
   later be adapted to a specific style.
   ```bash
   python pg.py idea --prompt "A futuristic city at sunset" --outputfile idea.txt
   ```
   The resulting text file can be used as the basis for other commands.

2. **Create a Picture in a Single Style**

   Assuming you have an idea prompt saved in `idea.txt`, generate an image
   using one of the styles defined in `support/styles.json`:
   ```bash
   python pg.py picbystyle -i idea.txt -p "add flying cars" -s Retro_80s --output_file out.png
   ```
   The command combines the text in `idea.txt`, any additional prompt text
   ("add flying cars" in the example) and the `Retro_80s` style to create the
   final prompt for DALL·E. The generated picture will be written to
   `out.png`.

3. **Generate Multiple Styles at Once**

   You can create several pictures with different styles in parallel using the
   `multistyle` command. Specify a comma‑separated list of styles or let the
   tool pick random ones for you:
   ```bash
   python pg.py multistyle -i idea.txt -s "Classic_Disney,Pixel_Art" \
       --output_file out.png -w 4
   ```
   or to use randomly chosen styles:
   ```bash
   python pg.py multistyle -i idea.txt -r 3 --output_file out.png
   ```
   The images will be saved with timestamps and the style name in the filename.

4. **Use an Idea File Directly**

   If you already have a complete prompt written in a file, you can generate a
   picture without any style adaptation using `picfrompromptfile`:
   ```bash
   python pg.py picfrompromptfile -i full_prompt.txt --output_file image.png
   ```

## Configuration

Runtime settings such as the GPT model, DALL·E model and picture size are
stored in `config.yaml`:
```yaml
MAIN_MODEL: "gpt-3.5-turbo-0125"
ART_MODEL: "dall-e-3"
PIC_SIZE: "1024x1024"
PIC_QUALITY: "Standard"
```
Adjust these values to suit your requirements.

The available art styles are listed in `support/styles.json`. Each style
contains a description and a color palette. When specifying the `--style`
argument, use the keys from this file (for example `Classic_Disney` or
`Anime`).

## Output Files

Images are saved with the current date and time added to their filename. The
helper functions also store intermediate prompts in the `temp` directory so you
can inspect the generated text that was sent to the API.

---

With these commands you can quickly experiment with different prompts and
styles to produce images using the DALL·E API. Consult `pg.py` for additional
options and use the `addstyle` command or edit `support/styles.json` to extend
it with your own styles.
