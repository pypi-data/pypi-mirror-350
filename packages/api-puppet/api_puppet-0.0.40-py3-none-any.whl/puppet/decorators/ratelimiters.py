import time


def uniform_rate_limiter(max_number_of_calls: int, period_in_seconds: int):
    """
    A decorator that limits the frequency at which a function can be called to a uniform rate.

    Args:
        :param max_number_of_calls: An integer representing the maximum number of times the decorated function can be called
                                    within a given period.
        :param period_in_seconds: An integer representing the length of the period in seconds within which the decorated
                                  function can be called a maximum number of times.
    :return: The inner decorator function that takes a function and returns a wrapper function that limits the frequency
             at which the function can be called.
    """
    max_sleep_time = 60.0
    last_execution = 0
    min_interval_between_calls: float = float(period_in_seconds) / float(max_number_of_calls)

    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal last_execution
            current_time = time.time()
            time_since_last_call = current_time - last_execution
            if time_since_last_call < min_interval_between_calls:
                sleep_time = min(max_sleep_time, min_interval_between_calls - time_since_last_call)
                time.sleep(sleep_time)

            response = func(*args, **kwargs)
            last_execution = time.time()

            return response
        return wrapper
    return inner_decorator


def burst_rate_limiter(max_number_of_calls: int, period_in_seconds: int):
    """
    Decorator that limits the number of calls to a function over a specified period of time. All the calls will be made
    without any interference until the max_number_of_calls has been reached. It will then wait until the period_in_seconds
    has been reached and will reset the number of calls allowed to max_number_of_calls.

    Args:
        max_number_of_calls: Maximum number of function calls allowed within the specified period of time.
        period_in_seconds: The time period within which the maximum number of calls are allowed.


    :return: A decorated function that limits the number of calls to the specified function over the specified period of time.
    """
    calls_left = max_number_of_calls
    end_of_window = time.time() + period_in_seconds

    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal calls_left
            nonlocal end_of_window

            if calls_left == 0:
                time_until_end_of_window = end_of_window - time.time()
                if time_until_end_of_window > 0:
                    time.sleep(time_until_end_of_window)

            if time.time() > end_of_window:
                calls_left = max_number_of_calls
                end_of_window = time.time() + period_in_seconds

            response = func(*args, **kwargs)
            calls_left -= 1

            return response
        return wrapper
    return inner_decorator
