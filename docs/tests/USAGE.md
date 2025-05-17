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
- style listing via the ``showstyles`` command

`tests/test_addstyle.py` covers the helper used by the `addstyle` command and
checks that duplicate styles are rejected. `tests/test_decorators.py` validates
the behaviour of the spinner and execution time decorators defined in
`support/decorators.py`. `tests/test_showstyles.py` exercises the new ``showstyles``
command.

## Adding Your Own Tests

Place new test modules inside the ``tests/`` directory. Use Python's ``unittest``
framework and mimic the existing files for reference. After creating a test
file, run ``python -m unittest discover -v -s tests`` to ensure everything still
passes.

When writing tests, stub out external modules such as ``openai`` or ``requests``
so the suite remains offline and deterministic. The current tests illustrate how
to replace these modules with simple objects before importing project code.
Give your test functions descriptive names beginning with ``test_`` and keep
assertions focused on one behaviour per test.

To try the command manually run:

```bash
python pg.py addstyle -n test -d "this is a test style description" -p "orange, blue"
```

Open `support/styles.json` and verify a new `"test"` entry exists. Remove that
block from the file to clean up if you no longer need the example.

