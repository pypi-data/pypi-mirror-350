import time


def retry_with_fixed_intervals(max_retries: int, interval_seconds: float, exceptions):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    """
    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, max_retries)
                    )
                    attempt += 1
                    time.sleep(interval_seconds)
            return func(*args, **kwargs)

        return wrapper
    return inner_decorator
