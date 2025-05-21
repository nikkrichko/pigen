# pigen

![CI](https://img.shields.io/github/actions/workflow/status/example/pigen/test.yml?label=CI)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Generate image prompts and pictures with OpenAI's DALL\u00b7E API using a simple command-line tool.

Utilities for crafting prompts, applying art styles and rendering images. The CLI `pg.py` also helps with story illustration workflows.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Usage](#quick-usage)
- [Configuration](#configuration)
- [Extending styles](#extending-stylesjson)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)
- [Documentation](#documentation)

## Features
- Generate idea prompts using ChatGPT
- Adapt prompts to predefined art styles
- Create single or multiple styled images
- Manage style definitions in `styles.json`
- Illustrate stories by generating scenes and characters

## Prerequisites
- Python 3.11+
- An OpenAI API key stored in the `OPENAI_API_KEY` environment variable

## Installation
1. Clone the repository and enter its folder:
   ```bash
   git clone <repo-url>
   cd pigen
   ```
2. Set up a Python virtual environment and install dependencies using the provided helper scripts. Choose the script matching your platform:
   - **Linux/macOS**
     ```bash
     ./scripts/install_linux.sh
     ```
   - **Windows**
     ```powershell
     powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1
     ```
   The scripts install all requirements, including the optional OpenTelemetry packages used for tracing support.
3. Set your `OPENAI_API_KEY` environment variable. In a Unix shell use `export OPENAI_API_KEY=<your-key>`.
4. (Optional) Run the preflight check to verify your installation:
   - **Linux/macOS**
     ```bash
     ./scripts/preflight.sh
     ```
   - **Windows**
     ```powershell
     powershell -ExecutionPolicy Bypass -File scripts/preflight.ps1
     ```
   The check runs automatically whenever `pg.py` starts but the scripts allow you to test your setup manually.

## Quick Usage
The CLI supports several commands for working with prompts and pictures. A few examples:
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
- Extract characters from a story file
  ```bash
  python pg.py characters -i story.txt -o characters.json
  ```

If you omit `--output_file` the image is saved inside `temp/` with a timestamped name like `010124_120000_style1.png`.

In short, the pipeline is:
1. Generate an idea text with `pg.py idea`.
2. Apply one or more styles using `picbystyle` or `multistyle`.
3. The final prompt is sent to DALL\u00b7E and the image is saved with a timestamp.

More detailed instructions can be found in:
- [Creating Pictures](docs/CREATING_PICTURES.md) - How to generate images with styles
- [Illustrating Stories](docs/ILLUSTRATING_STORIES.md) - How to analyze stories for illustration

## Configuration
Runtime options are stored in `config.yaml`. Key settings include:
- `MAIN_MODEL` – ChatGPT model used for prompt generation. Switch this to a GPT‑4 model if your account allows it.
- `ART_MODEL` – DALL\u00b7E version for images (currently `dall-e-3`).
- `PIC_SIZE` – Desired output size such as `1024x1024` or `1792x1024`.
- `PIC_QUALITY` – Set to `Standard` or `hd` for higher fidelity pictures.
- `LOG_LEVEL` – Console log verbosity.
- `ENABLE_OPENTELEMETRY` – Enable OpenTelemetry tracing when `true`.
- `OTEL_SERVICE_NAME` – Service name used for OpenTelemetry spans.
- `OTEL_EXPORTER_OTLP_ENDPOINT` – Destination OTLP endpoint for traces.

Adjust these values to fit your workflow and API quota.

## Extending styles.json
The file `support/styles.json` holds all available art styles. Use `pg.py addstyle` to add one interactively or edit the JSON manually. A minimal entry looks like:
```json
{
  "Comic_Book": {
    "description": "Bold ink lines with halftone shading.",
    "palette": "Strong primaries with black and white"
  }
}
```
After saving you can reference the new style with `-s Comic_Book`.

## Running Tests
Mock-based tests covering each pipeline step live in the `tests/` folder. Use the helper scripts to run them after setting up your environment:
- **Linux/macOS**
  ```bash
  ./scripts/run_tests.sh
  ```
- **Windows**
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/run_tests.ps1
  ```
More details can be found in [docs/tests/USAGE.md](docs/tests/USAGE.md).

## Contributing
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to submit patches and feature requests.

## License
This project is licensed under the [MIT License](LICENSE).

## Documentation
| File | Description |
|------|-------------|
| [docs/CREATING_PICTURES.md](docs/CREATING_PICTURES.md) | Step-by-step guide for generating images with different styles |
| [docs/ILLUSTRATING_STORIES.md](docs/ILLUSTRATING_STORIES.md) | Explain how to break down a story into scenes and characters |
| [docs/INSTALLATION.md](docs/INSTALLATION.md) | Alternative installation instructions for all platforms |
| [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) | Details on configuration, logging and test execution |
| [docs/tests/USAGE.md](docs/tests/USAGE.md) | Instructions for running the unit tests directly |

