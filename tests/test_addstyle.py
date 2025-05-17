import sys
import types
import json
import tempfile
import unittest

# Stub external modules used in support.functions
openai_stub = types.ModuleType('openai')
openai_stub.Client = object
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

if 'support.decorators' in sys.modules:
    decorators_stub = sys.modules['support.decorators']
else:
    decorators_stub = types.ModuleType('support.decorators')
    sys.modules['support.decorators'] = decorators_stub
decorators_stub.spinner_decorator = lambda f: f
decorators_stub.execution_time_decorator = lambda f: f

import support.functions as f


class AddStyleTests(unittest.TestCase):
    def test_add_style_and_duplicates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            styles_path = f"{tmpdir}/styles.json"
            with open(styles_path, "w", encoding="utf-8") as fh:
                json.dump({}, fh)

            f.add_style_to_file("test", "desc", "palette", file_path=styles_path)
            with open(styles_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            self.assertIn("test", data)
            self.assertEqual(data["test"], {"description": "desc", "palette": "palette"})

            with self.assertRaises(ValueError):
                f.add_style_to_file("test", "other", "palette2", file_path=styles_path)


if __name__ == "__main__":
    unittest.main()
