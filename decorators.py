import itertools
import sys
import threading
import time
import datetime
import random
import logging
from functools import wraps


def _get_random_spinner_list():
    """Generate a list of spinner frames based on the current hour."""
    size = datetime.datetime.now().hour

    spec = ['[', '@', '#', '$', '%', '^', 'x', '<', '>', '(o)', '=', '+', ';', ':', '<|>', '{?}', '[A]']
    wrapper_chars = ['.', '_', '-', '~']

    spinning_sign = random.choice(spec)
    wrap_char = random.choice(wrapper_chars)
    spin_list = []
    for i in range(size):
        dots_after = wrap_char * i
        dots_before = wrap_char * (size - i)
        line = dots_before + spinning_sign + dots_after
        spin_list.append(line)

    for i in range(size):
        dots_after = wrap_char * (size - i)
        dots_before = wrap_char * i
        line = dots_before + spinning_sign + dots_after
        spin_list.append(line)

    return spin_list


def spinner_decorator(method):
    def spinner(*args, **kwargs):
        spinner_chars = _get_random_spinner_list()
        stop_spinner = threading.Event()
        spinner_thread = None

        def display_spinner():
            for char in itertools.cycle(spinner_chars):
                sys.stdout.write('\r' + char)
                sys.stdout.flush()
                if stop_spinner.is_set():
                    break
                time.sleep(0.1)

        try:
            spinner_thread = threading.Thread(target=display_spinner)
            spinner_thread.daemon = True
            spinner_thread.start()
            result = method(*args, **kwargs)
            return result
        except Exception as e:
            if spinner_thread is not None:
                stop_spinner.set()
                spinner_thread.join()
                sys.stdout.write('\r')
                sys.stdout.flush()
            raise e
        finally:
            if spinner_thread is not None:
                stop_spinner.set()
                spinner_thread.join()
                sys.stdout.write('\r')
                sys.stdout.flush()

    return spinner


def execution_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\tExecution time for '{func.__name__}': {execution_time:.2f} seconds")
        return result

    return wrapper


def log_function_info_and_debug(logger=logging.getLogger()):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(f"{func.__name__} - executed in seconds - {end_time - start_time:.6f}")
            logger.debug(f"{func.__name__} - args: {args}, kwargs: {kwargs}")
            return result
        return wrapper
    return decorator
