import itertools
import sys
import threading
import time


def spinner_decorator(method):
    def spinner(*args, **kwargs):
        # Define the spinner characters

        spinner_chars = ['+......', '.+.....', '..+....', '...+...', '....+..','.....+.','......+','.....+.', '....+..', '...+...', '..+....','.+.....']

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
