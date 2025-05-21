import logging
from functools import wraps

import support.Configurator as Config

try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    OTEL_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    OTEL_AVAILABLE = False

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        config = Config.Config()
        level_name = str(config.get('LOG_LEVEL')).upper()
        self.log_level = getattr(logging, level_name, logging.INFO)
        self.logger = logging.getLogger("pigen")
        self.logger.setLevel(self.log_level)

        self.tracer = None
        try:
            enable_otel = str(config.get('ENABLE_OPENTELEMETRY')).lower() == 'true'
        except KeyError:
            enable_otel = False
        if enable_otel and OTEL_AVAILABLE:
            try:
                service_name = str(config.get('OTEL_SERVICE_NAME'))
            except KeyError:
                service_name = 'pigen'
            try:
                endpoint = str(config.get('OTEL_EXPORTER_OTLP_ENDPOINT'))
            except KeyError:
                endpoint = 'http://localhost:4318'
            provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
            exporter = OTLPSpanExporter(endpoint=endpoint)
            provider.add_span_processor(BatchSpanProcessor(exporter))
            trace.set_tracer_provider(provider)
            self.tracer = trace.get_tracer(service_name)
            try:  # pragma: no cover - optional instrumentation
                LoggingInstrumentor().instrument(set_logging_format=True)
            except Exception:
                pass

        # Only add handler if there are none already
        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self._initialized = True

    def log(self, message, level=None):
        level = level or self.log_level
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        self.logger.log(level, message)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

def delog(level="DEBUG"):
    """Decorator to log function start/finish at the given level.

    Parameters
    ----------
    level : str, optional
        Logging level name ("INFO" or "DEBUG"), by default "DEBUG".
    """
    logger = Logger()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_method = logger.info if level.upper() == "INFO" else logger.debug
            log_method(f"{func.__name__} - started")
            try:
                result = func(*args, **kwargs)
                log_method(f"{func.__name__} - finished")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} - error: {e}")
                raise

        return wrapper

    return decorator
