import sys
import types
import json
import tempfile
import os
import unittest
from unittest import mock
from click.testing import CliRunner

# Stub external modules used in pg
openai_stub = types.ModuleType('openai')
openai_stub.Client = object
openai_stub.OpenAI = lambda: types.SimpleNamespace()
sys.modules['openai'] = openai_stub

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

icecream_stub = types.ModuleType('icecream')
icecream_stub.ic = lambda *a, **k: None
sys.modules['icecream'] = icecream_stub

urllib3_stub = types.ModuleType('urllib3')
urllib3_stub.disable_warnings = lambda *a, **k: None
urllib3_stub.exceptions = types.SimpleNamespace(NotOpenSSLWarning=type('x',(object,),{}))
sys.modules['urllib3'] = urllib3_stub

yaml_stub = types.ModuleType('yaml')
yaml_stub.safe_load = lambda *a, **k: {}
sys.modules['yaml'] = yaml_stub

import pg

class CharactersCliTests(unittest.TestCase):
    def test_characters_command_writes_file(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, 'story.txt')
            output_path = os.path.join(tmpdir, 'chars.json')
            with open(input_path, 'w', encoding='utf-8') as fh:
                fh.write('Once upon a time')
            sample = {'Hero': {'info': 'x'}}
            with mock.patch('support.story_utils.extract_characters', return_value=sample):
                pg.model_to_chat = 'test-model'
                result = runner.invoke(pg.cli, ['characters', '-i', input_path, '-o', output_path])
            self.assertEqual(result.exit_code, 0)
            with open(output_path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            self.assertEqual(data, sample)

if __name__ == '__main__':
    unittest.main()
