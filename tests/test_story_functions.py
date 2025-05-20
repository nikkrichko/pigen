import sys
import types
import json
import unittest
from unittest.mock import patch

# Stub external modules used in story utilities
openai_stub = types.ModuleType('openai')
openai_stub.Client = object
openai_stub.OpenAI = lambda *a, **k: types.SimpleNamespace()
sys.modules['openai'] = openai_stub

gpt_tools_stub = types.ModuleType('reseach.gpt_tools')
class DummyGptClient:
    def run_prompt(self, *a, **k):
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="{}"))])
gpt_tools_stub.GptClient = DummyGptClient
sys.modules['reseach.gpt_tools'] = gpt_tools_stub

if 'requests' in sys.modules:
    requests_stub = sys.modules['requests']
else:
    requests_stub = types.ModuleType('requests')
    sys.modules['requests'] = requests_stub
requests_stub.get = lambda url: types.SimpleNamespace(content=b'data')

if 'support.logger' in sys.modules:
    logger_stub = sys.modules['support.logger']
else:
    logger_stub = types.ModuleType('support.logger')
    sys.modules['support.logger'] = logger_stub
logger_stub.delog = lambda: (lambda f: f)
class DummyLogger:
    def __init__(self, *a, **k):
        self.logger = None
    def log(self, *a, **k):
        pass
logger_stub.Logger = DummyLogger

if 'support.decorators' in sys.modules:
    decorators_stub = sys.modules['support.decorators']
else:
    decorators_stub = types.ModuleType('support.decorators')
    sys.modules['support.decorators'] = decorators_stub
decorators_stub.spinner_decorator = lambda f: f
decorators_stub.execution_time_decorator = lambda f: f
decorators_stub.log_function_info_and_debug = lambda logger=None: (lambda f: f)

import support.story_utils as sf
import support.character_description
import support.sceneDescription


class StoryFunctionTests(unittest.TestCase):
    def test_validate_story(self):
        expected = {"is_story": True, "reason": "ok", "estimated_scenes": 2}
        dummy_client = types.SimpleNamespace(
            chat=types.SimpleNamespace(
                completions=types.SimpleNamespace(
                    create=lambda **kwargs: types.SimpleNamespace(
                        choices=[types.SimpleNamespace(
                            message=types.SimpleNamespace(content=json.dumps(expected))
                        )]
                    )
                )
            )
        )
        result = sf.validate_story("text", dummy_client, "model")
        self.assertEqual(result, expected)

    def test_extract_characters(self):
        chars_response = {"characters": ["Alice", "Bob"]}
        dummy_client = types.SimpleNamespace(
            chat=types.SimpleNamespace(
                completions=types.SimpleNamespace(
                    create=lambda **kwargs: types.SimpleNamespace(
                        choices=[types.SimpleNamespace(
                            message=types.SimpleNamespace(content=json.dumps(chars_response))
                        )]
                    )
                )
            )
        )
        with patch('support.character_description.CharacterAppearance.generate_appearance',
                   side_effect=lambda name: {"name": name}), \
             patch('support.character_description.CharacterAppearance.save_appearance_to_file',
                   return_value=True):
            result = sf.extract_characters("story", dummy_client, "model")
        expected = {"Alice": {"name": "Alice"}, "Bob": {"name": "Bob"}}
        self.assertEqual(result, expected)

    def test_generate_scenes(self):
        scenes_dict = {
            "1": {"description": "d1", "characters": ["A"], "setting": "s1"},
            "2": {"description": "d2", "characters": ["B"], "setting": "s2"}
        }
        dummy_client = object()
        with patch('support.sceneDescription.SceneGenerator') as MockSG:
            instance = MockSG.return_value
            instance.generate_scenes_from_story.return_value = scenes_dict
            result = sf.generate_scenes("story", 2, {"A": {}, "B": {}}, dummy_client, "model")
            MockSG.assert_called_once_with(gpt_model="model")
            instance.generate_scenes_from_story.assert_called_once_with("story", 2, ["A", "B"])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["scene_number"], 1)
        self.assertEqual(result[1]["scene_number"], 2)


if __name__ == '__main__':
    unittest.main()
