import unittest
from unittest import mock
import datetime
import sys
import importlib.util
from pathlib import Path

# Load support.decorators directly to avoid importing the rest of the package
spec = importlib.util.spec_from_file_location(
    "support.decorators", Path(__file__).resolve().parents[1] / "support" / "decorators.py"
)
decorators = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decorators)
sys.modules['support.decorators'] = decorators


class DecoratorTests(unittest.TestCase):
    def setUp(self):
        # Reload the decorators module in case other tests modified it
        spec = importlib.util.spec_from_file_location(
            "support.decorators",
            Path(__file__).resolve().parents[1] / "support" / "decorators.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules['support.decorators'] = module
        global decorators
        decorators = module

    def test_get_random_spinner_list(self):
        fixed_dt = datetime.datetime(2024, 1, 1, 0, 0, 0)

        class DummyDateTime(datetime.datetime):
            @classmethod
            def now(cls):
                return fixed_dt.replace(hour=5)

        with mock.patch.object(decorators.datetime, 'datetime', DummyDateTime), \
             mock.patch.object(decorators.random, 'choice', side_effect=lambda seq: seq[0]):
            result = decorators._get_random_spinner_list()

        expected = []
        wrap = '.'
        sign = '['
        size = 5
        for i in range(size):
            expected.append(wrap * (size - i) + sign + wrap * i)
        for i in range(size):
            expected.append(wrap * i + sign + wrap * (size - i))
        self.assertEqual(result, expected)

    def test_spinner_decorator_returns_value(self):
        @decorators.spinner_decorator
        def sample(x):
            return x + 1

        with mock.patch.object(decorators, '_get_random_spinner_list', return_value=['-', '|']), \
             mock.patch.object(decorators.time, 'sleep'), \
             mock.patch.object(decorators.sys, 'stdout'):
            self.assertEqual(sample(1), 2)

    def test_execution_time_decorator_prints(self):
        from io import StringIO
        from contextlib import redirect_stdout

        with mock.patch.object(decorators.time, 'time', side_effect=[0, 1]):
            buf = StringIO()
            with redirect_stdout(buf):
                @decorators.execution_time_decorator
                def func():
                    return 'ok'

                self.assertEqual(func(), 'ok')

            output = buf.getvalue()

        self.assertIn("Execution time for 'func': 1.00 seconds", output)

    def test_log_function_info_and_debug(self):
        class DummyLogger:
            def __init__(self):
                self.info_msgs = []
                self.debug_msgs = []

            def info(self, msg):
                self.info_msgs.append(msg)

            def debug(self, msg):
                self.debug_msgs.append(msg)

        logger = DummyLogger()

        with mock.patch.object(decorators.time, 'time', side_effect=[0, 1]):
            @decorators.log_function_info_and_debug(logger)
            def func(a, b=1):
                return a + b

            self.assertEqual(func(2, b=3), 5)

        self.assertEqual(len(logger.info_msgs), 1)
        self.assertTrue(logger.info_msgs[0].startswith('func - executed in seconds - '))
        self.assertEqual(logger.debug_msgs[0], "func - args: (2,), kwargs: {'b': 3}")


if __name__ == '__main__':
    unittest.main()
