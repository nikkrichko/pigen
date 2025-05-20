# Illustrating Stories

This guide explains how to use the `ill-story` command to generate
character descriptions and scene breakdowns from a text file.

The command reads a story, identifies characters, and produces a JSON
structure describing each key scene. Optionally, you can provide a JSON
file with pre-generated characters using the `--charfile` option.

## Basic Usage

```bash
python pg.py ill-story -i story.txt -o illustration.json -n 8
```

The resulting `illustration.json` contains the story summary, characters,
and scenes. Each scene includes information about the setting, objects and
which characters appear.

## Reusing Character Descriptions

If you already have character descriptions saved in a file, pass it with
`-c` or `--charfile` to skip character generation:

```bash
python pg.py ill-story -i story.txt -o illustration.json -n 8 -c characters.json
```

The JSON must map character names to the structure returned by the
`CharacterDescription` model. If the file cannot be parsed or does not
match the expected schema the command stops with an error message.
