import itertools
import sys
import threading
import time
import datetime
import random


def _get_random_spinner_list():
    """

    This method returns a list of strings with spinning signs.

    Example usage:
        spinner_list = _get_random_spinner_list()

    Explanation:
        - The method first retrieves the current hour using the `datetime` module.
        - It then initializes two lists: `spec` and `wrapper_chars`, containing special symbols and wrapper characters respectively.
        - The spinning sign is randomly chosen from the `spec` list.
        - The wrapper character is randomly chosen from the `wrapper_chars` list.
        - The method then generates strings of spinning signs, with the number of repeated wrapper characters decreasing as the index increases. The generated strings are appended to the
    * `spin_list`.
        - Similarly, the method generates strings of spinning signs with the number of repeated wrapper characters decreasing as the index decreases. These strings are also appended to the
    * `spin_list`.
        - Finally, the `spin_list` is returned.

    Note:
        - This method uses the `random` and `datetime` modules, so they need to be imported before using this method.

    """
    size = datetime.datetime.now().hour

    # get list numbers between 0 and 9 and from all special symbols
    spec = ['!', '@', '#', '$', '%', '^', '><', '<>', '(o)', '=', '+', ';', ':', '<|>', '{?}', '[A]']
    wrapper_chars = ['.', '_', '-', '*']
    # get random from list

    spinning_sign = random.choice(spec)
    wrap_char = random.choice(wrapper_chars)
    spin_list = []
    for i in range(size):
        # Generate a string with decreasing numbers of dots
        dots_after = wrap_char * (i)
        dots_before = wrap_char * (size - i)
        # Add the spinning sign to the generated string
        line = dots_before + spinning_sign + dots_after
        spin_list.append(line)

    for i in range(size):
        # Generate a string with decreasing numbers of dots
        dots_after = wrap_char * (size - i)
        dots_before = wrap_char * (i)
        # Add the spinning sign to the generated string
        line = dots_before + spinning_sign + dots_after
        spin_list.append(line)

    return spin_list


def spinner_decorator(method):
    def spinner(*args, **kwargs):
        # Define the spinner characters
        spinner_chars = _get_random_spinner_list()

        # Initialize the stop flag
        stop_spinner = threading.Event()

        # Function to display the spinner
        def display_spinner():
            for char in itertools.cycle(spinner_chars):
                sys.stdout.write('\r' + char)
                sys.stdout.flush()
                if stop_spinner.is_set():
                    break
                time.sleep(0.1)

        try:
            # Start a background thread to display the spinner
            spinner_thread = threading.Thread(target=display_spinner)
            spinner_thread.daemon = True
            spinner_thread.start()

            # Call the original method
            result = method(*args, **kwargs)

            return result
        except Exception as e:
            # Handle exceptions
            if spinner_thread is not None:
                stop_spinner.set()  # Set the stop flag to stop the spinner
                spinner_thread.join()
            sys.stdout.write('\r')
            sys.stdout.flush()
            raise e
        finally:
            # Ensure the spinner thread is stopped and the line is cleared
            if spinner_thread is not None:
                stop_spinner.set()  # Set the stop flag to stop the spinner
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
        print(f"\t\tExecution time for '{func.__name__}': {execution_time:.2f} seconds")
        return result

    return wrapper
