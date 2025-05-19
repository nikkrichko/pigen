import logging
import support.Configurator as Config
import time

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
        self.log_level = config.get('LOG_LEVEL')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)

        # Only add handler if there are none already
        if not self.logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self._initialized = True

    def log(self, message):
        if self.log_level == "DEBUG":
            self.logger.debug(message)
        else:
            self.logger.info(message)

def delog():
    logger = Logger()

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()

            logger.log(f'{func.__name__} - started')

            result = func(*args, **kwargs)

            end_time = time.time()
            logger.log(f'{func.__name__} - finished in {end_time - start_time:.2f} seconds')

            if logger.log_level == "DEBUG":
                debug_message = f'Execution time for {func.__name__}: {end_time - start_time:.2f} seconds -- {func.__name__} - args: {args}, kwargs: {kwargs}'
                logger.log(debug_message)

            return result
        return wrapper
    return decorator
