import importlib
import sys
import types
import unittest


class LoggerConfigTests(unittest.TestCase):
    """Ensure logger loads even when OpenTelemetry is requested."""

    def test_logger_initializes_without_otel_packages(self):
        dummy_cfg = {
            "LOG_LEVEL": "INFO",
            "ENABLE_OPENTELEMETRY": True,
        }

        class DummyConfig:
            def __init__(self):
                pass

            def get(self, key):
                return dummy_cfg.get(key)

        cfg_module = sys.modules.get("support.Configurator")
        if cfg_module is None:
            cfg_module = types.ModuleType("support.Configurator")
            sys.modules["support.Configurator"] = cfg_module

        cfg_module.Config = DummyConfig

        if "support.logger" in sys.modules:
            del sys.modules["support.logger"]
        logger_module = importlib.import_module("support.logger")
        inst = logger_module.Logger()
        self.assertIsNotNone(inst)


if __name__ == "__main__":
    unittest.main()

