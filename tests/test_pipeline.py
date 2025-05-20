import sys
import types
import datetime
import unittest
from unittest import mock

# Stub external modules before importing project code
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

import support.file_utils as f_file
import support.style_utils as f_style
import support.image_utils as f_image


class PipelineTests(unittest.TestCase):
    def test_save_text_to_file(self):
        with self.subTest():
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                path = f"{tmpdir}/out.txt"
                f_file.save_text_to_file("hello", path)
                with open(path) as fh:
                    self.assertEqual(fh.read(), "hello")

    def test_replace_last_path_part_with_datetime(self):
        fixed_dt = datetime.datetime(2024, 1, 1, 12, 0, 0)

        class DummyDateTime(datetime.datetime):
            @classmethod
            def now(cls):
                return fixed_dt

        orig = f_file.datetime.datetime
        f_file.datetime.datetime = DummyDateTime
        try:
            result = f_file.replace_last_path_part_with_datetime("/tmp/file.txt", "Style")
        finally:
            f_file.datetime.datetime = orig
        self.assertTrue(result.endswith("_Style_file.txt"))
        self.assertIn("2024-01-01_12-00-00", result)

    def test_default_output_file(self):
        fixed_dt = datetime.datetime(2024, 1, 1, 12, 0, 0)

        class DummyDateTime(datetime.datetime):
            @classmethod
            def now(cls):
                return fixed_dt

        orig = f_file.datetime.datetime
        f_file.datetime.datetime = DummyDateTime
        try:
            import tempfile
            import os
            with tempfile.TemporaryDirectory() as tmpdir:
                with mock.patch.object(f_file, "TEMP_DIR", tmpdir):
                    result = f_file.default_output_file("Style")
                    expected = os.path.join(tmpdir, "010124_120000_Style.png")
                    self.assertEqual(result, expected)
        finally:
            f_file.datetime.datetime = orig

    def test_generate_and_save_idea(self):
        calls = {}

        def fake_generate_idea(prompt):
            calls["prompt"] = prompt
            return "idea"

        def fake_get_prompt_result(client, prompt, model_to_chat, gpt_role=""):
            calls["model"] = model_to_chat
            calls["gpt_role"] = gpt_role
            return "final idea"

        saved = {}

        def fake_save(text, filename):
            saved[filename] = text

        with mock.patch.object(f_style, "generate_idea", fake_generate_idea), \
             mock.patch.object(f_style, "get_prompt_result", fake_get_prompt_result), \
             mock.patch.object(f_style, "save_text_to_file", fake_save):
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                path = f"{tmpdir}/idea.txt"
                result = f_style.generate_and_save_idea("prompt text", path, object(), "gpt")
                self.assertEqual(calls["prompt"], "prompt text")
                self.assertEqual(calls["model"], "gpt")
                self.assertEqual(saved[path], "final idea")
                self.assertEqual(result, "final idea")

    def test_generate_adopted_prompt(self):
        with mock.patch.object(f_style, "adopt_style", lambda base, style, add: "styled"), \
             mock.patch.object(f_style, "get_dalle_prompt_based_on_input", lambda client, text, model: "final"):
            saved = {}
            def fake_save(text, filename):
                saved[filename] = text

            with mock.patch.object(f_style, "save_text_to_file", fake_save):
                import tempfile
                with tempfile.TemporaryDirectory() as tmpdir:
                    f_style.ADOPT_PROMPT_TXT_PATH = f"{tmpdir}/adopt.txt"
                    f_style.ADOPTED_PROMPT_PATH = f"{tmpdir}/final.txt"
                    result = f_style.generate_adopted_prompt("extra", "idea", "Anime", object(), "gpt")
                    self.assertEqual(result, "final")
                    self.assertEqual(saved[f_style.ADOPT_PROMPT_TXT_PATH], "styled")
                    self.assertEqual(saved[f_style.ADOPTED_PROMPT_PATH], "final")

    def test_generate_image(self):
        class DummyImages:
            def generate(self, **kwargs):
                return types.SimpleNamespace(data=[types.SimpleNamespace(url="http://x")])

        dummy_client = types.SimpleNamespace(images=DummyImages())
        with mock.patch.object(requests_stub, "get", lambda url: types.SimpleNamespace(content=b"img")):
            result = f_image.generate_image("prompt", dummy_client)
        self.assertEqual(result, b"img")

    def test_save_picture(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            path = f"{tmpdir}/img.png"
            f_image.save_picture(path, b"abc")
            with open(path, "rb") as fh:
                self.assertEqual(fh.read(), b"abc")

    def test_log_prompt_output(self):
        fixed_dt = datetime.datetime(2024, 1, 1, 12, 0, 0)

        class DummyDateTime(datetime.datetime):
            @classmethod
            def now(cls):
                return fixed_dt

        orig = f_file.datetime.datetime
        f_file.datetime.datetime = DummyDateTime
        import tempfile
        import os
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                cwd = os.getcwd()
                os.chdir(tmpdir)
                try:
                    rel_path = f_file.log_prompt_output("idea", "p", "o")
                    log_path = os.path.join(tmpdir, rel_path)
                finally:
                    os.chdir(cwd)
                with open(log_path) as fh:
                    content = fh.read()
                self.assertIn("prompt:", content)
                self.assertIn("output:", content)
                self.assertIn("p", content)
                self.assertIn("o", content)
        finally:
            f_file.datetime.datetime = orig


if __name__ == "__main__":
    unittest.main()
