import logging
import support.Configurator as Config

class Logger:
    def __init__(self):
        config = Config.Config()
        log_level = config.get('LOG_LEVEL')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, message):
        if self.logger.level == logging.DEBUG:
            self.logger.debug(message)
        else:
            self.logger.info(message)

def delog():
    logger = Logger()
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.log(f'Calling function: {func.__name__}')
            result = func(*args, **kwargs)
            logger.log(f'Function {func.__name__} finished')
            return result
        return wrapper
    return decorator