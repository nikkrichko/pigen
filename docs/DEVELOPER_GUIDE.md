# Developer Guide

This document provides additional instructions for developers working on `pigen`. It explains how to configure logging, run the CLI commands, prepare test data and execute the unit tests for each command.

## Environment Setup

Create a virtual environment and install the project requirements using the helper scripts:

```bash
./scripts/install_linux.sh      # Linux/macOS
# or
powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1
```

The scripts install all dependencies listed in `requirements.txt`, including the optional OpenTelemetry packages used for tracing.

## Configuring the Log Level

Logging behaviour is controlled through `config.yaml`. Set the `LOG_LEVEL` key to the desired verbosity, for example:

```yaml
LOG_LEVEL: "DEBUG"
```

Valid values are the standard Python log levels (`DEBUG`, `INFO`, `WARNING`, etc.). The `Logger` class in `support/logger.py` reads this value on startup.

If you set `ENABLE_OPENTELEMETRY: true` in `config.yaml` the logger will send
trace data using the OTLP protocol. Configure the `OTEL_SERVICE_NAME` and
`OTEL_EXPORTER_OTLP_ENDPOINT` keys to match your collector.

## Running CLI Commands

All commands are exposed through `pg.py`. The most commonly used commands are listed below. Replace file names with your own paths as needed.

- **idea** – generate a detailed prompt from a short phrase or text file
  ```bash
  python pg.py idea -p "A robot on the moon" -o idea.txt
  ```
- **picbystyle** – create a picture using one style
  ```bash
  python pg.py picbystyle -i idea.txt -s Retro_80s -o output.png
  ```
- **multistyle** – generate multiple styled pictures at once
  ```bash
  python pg.py multistyle -i idea.txt -s "Comic_Book,Pixel_Art" -o out.png
  ```
- **picfrompromptfile** – render an image directly from a full prompt
  ```bash
  python pg.py picfrompromptfile -i full_prompt.txt -o image.png
  ```
- **addstyle** – append a style entry to `support/styles.json`
  ```bash
  python pg.py addstyle -n Test -d "short description" -p "orange, blue"
  ```
- **showstyles** – list available styles
  ```bash
  python pg.py showstyles -d -p
  ```
- **characters** – extract characters from a story file
  ```bash
  python pg.py characters -i story.txt -o characters.json
  ```
- **ill-story** – generate scenes and characters for illustration
  ```bash
  python pg.py ill-story -i story.txt -o illustration.json -n 8
  ```

## Preparing Test Data

The test suite creates temporary files automatically, so no additional setup is required. To experiment manually you can create small text or JSON files:

- `idea.txt` – used by `picbystyle`, `multistyle` and similar commands.
- `full_prompt.txt` – a full prompt for `picfrompromptfile`.
- `story.txt` – input for `characters` and `ill-story`.
- `characters.json` – optional character descriptions consumed by `ill-story`.
- `styles.json` – styles for `addstyle` and `showstyles` (located in `support/`).

## Running Tests

All tests live in the `tests/` directory and run offline. Execute the complete suite with:

```bash
python -m unittest discover -v -s tests
```

Each major command has a dedicated test module. Run an individual file to test a command in isolation:

```bash
python -m unittest tests/test_addstyle.py       # addstyle
python -m unittest tests/test_showstyles.py     # showstyles
python -m unittest tests/test_characters_cli.py # characters
python -m unittest tests/test_ill_story.py      # ill-story
```

`tests/test_pipeline.py` exercises helper functions used by `idea`, `picbystyle` and related commands. The other modules (`test_scene_*`) cover the scene generator utilities.

