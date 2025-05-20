# Creating Pictures with `pigen`

This guide explains how to use the command line interface provided by the
`pigen` project to generate images with different styles using OpenAI's
API. It assumes you already have Python 3 installed and an OpenAI API key.

## Pipeline Overview

The tool follows a simple pipeline to transform your idea into a finished
picture. Understanding each stage will help you customize the results:

1. **Idea Generation** – Using the `idea` command, a short concept is
   expanded into a detailed description. The helper function
   `generate_and_save_idea` (defined in `support/style_utils.py`) sends your
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
   If ``--output_file`` is omitted they are written to the ``temp`` directory
   with names like ``010124_120000_Retro_80s.png``.

4. **Show Available Styles**

   View all style names stored in ``support/styles.json``. Add ``-d`` to include
   descriptions and ``-p`` to display palettes.
   ```bash
   python pg.py showstyles -d -p
   ```

5. **Use an Idea File Directly**

   If you already have a complete prompt written in a file, you can generate a
   picture without any style adaptation using `picfrompromptfile`:
   ```bash
   python pg.py picfrompromptfile -i full_prompt.txt --output_file image.png
   ```
   When no ``--output_file`` is specified, the picture is placed in ``temp/``
   using a timestamped name such as ``010124_120000.png``.

## Configuration

Runtime settings such as the GPT model, DALL·E model and picture size are
stored in `config.yaml`:
```yaml
MAIN_MODEL: "gpt-3.5-turbo-0125"
ART_MODEL: "dall-e-3"
PIC_SIZE: "1024x1024"
PIC_QUALITY: "Standard"
```
Adjust these values to suit your requirements. Each option has the following meaning:

- **MAIN_MODEL** – the ChatGPT model used for text prompts. Replace with a GPT‑4 model string
  if you need higher quality text generation.
- **ART_MODEL** – the DALL·E model leveraged for image creation.
- **PIC_SIZE** – output resolution. Valid values include `1024x1024`, `1024x1792` and `1792x1024`.
- **PIC_QUALITY** – either `Standard` or `hd` to request higher fidelity images.
- **LOG_LEVEL** – controls the verbosity of the application's logging.

The available art styles are listed in `support/styles.json`. Each style
contains a description and a color palette. When specifying the `--style`
argument, use the keys from this file (for example `Classic_Disney` or
`Anime`).

### Adding Custom Styles

You can extend `support/styles.json` manually or via the `addstyle` command.
Below is a minimal manual snippet:

```json
{
  "Comic_Book": {
    "description": "Bold ink lines with halftone shading.",
    "palette": "Strong primaries with black and white"
  }
}
```

After editing the file you can reference the new style with `-s Comic_Book` in
any of the picture commands.

## Output Files

Images are saved with the current date and time added to their filename. The
helper functions also store intermediate prompts in the `temp` directory so you
can inspect the generated text that was sent to the API.

---

With these commands you can quickly experiment with different prompts and
styles to produce images using the DALL·E API. Consult `pg.py` for additional
options and use the `addstyle` command (which requires `--name`, `--description`
and `--palette`) or edit `support/styles.json` to extend it with your own
styles.
