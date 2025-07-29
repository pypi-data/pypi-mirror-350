import time


class TimeOutException(Exception):
    pass


def timeout(seconds_before_timeout: int, message: str = None):
    max_time = time.time() + seconds_before_timeout

    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            if time.time() >= max_time:
                raise TimeOutException(f"Timeout occured on '{func.__name__}' after {seconds_before_timeout} seconds. {message or ''}")

            return func(*args, **kwargs)
        return wrapper

    return inner_decorator
