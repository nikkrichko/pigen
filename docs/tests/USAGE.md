# Running the Test Suite

This project uses Python's built-in **unittest** module. All external API calls
are mocked so the tests run offline and do not require a valid OpenAI key.

1. Install the project requirements. From the repository root run:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute the tests:
   ```bash
   python -m unittest discover -v -s tests
   ```
   All test files are located in the `tests/` directory.

The tests verify each step of the pipeline:

- idea generation and saving to a file
- adoption of styles and prompt preparation
- image generation
- utility helpers such as saving text or pictures

