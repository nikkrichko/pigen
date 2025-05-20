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

class ShowStylesTests(unittest.TestCase):
    def test_showstyles_lists_names(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            style_path = os.path.join(tmpdir, 'styles.json')
            with open(style_path, 'w', encoding='utf-8') as fh:
                json.dump({'Test': {'description': 'desc', 'palette': 'pal'}}, fh)
            def loader(fp=style_path):
                with open(style_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            with mock.patch('support.style_utils.load_styles', loader):
                result = runner.invoke(pg.cli, ['showstyles'])
            self.assertIn('Style: Test', result.output)

    def test_showstyles_with_options(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            style_path = os.path.join(tmpdir, 'styles.json')
            with open(style_path, 'w', encoding='utf-8') as fh:
                json.dump({'Demo': {'description': 'd', 'palette': 'p'}}, fh)
            def loader(fp=style_path):
                with open(style_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            with mock.patch('support.style_utils.load_styles', loader):
                result = runner.invoke(pg.cli, ['showstyles', '-d', '-p'])
            self.assertIn('Description: d', result.output)
            self.assertIn('Palette: p', result.output)

if __name__ == '__main__':
    unittest.main()
