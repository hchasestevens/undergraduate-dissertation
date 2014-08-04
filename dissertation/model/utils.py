"""Contains utilities and other common or orphaned functions."""

import contextlib
import functools


@contextlib.contextmanager
def ignore(*exceptions):
    """Pass on the given exceptions."""
    try:
        yield
    except exceptions:
        pass


def cached(func):
    """
    Cache given function, performing constant-time lookup when given previously
    computed values.
    """
    cache = {}
    @functools.wraps(func)
    def cached_func(*args, **kwargs):
        key = args, tuple(kwargs.items())
        with ignore(KeyError):
            return cache[key]
        cache[key] = func(*args, **kwargs)
        return cache[key]
    return cached_func


def nth_argument_factory(arg_n):
    """Create an nth_argument decorator factory."""
    def nth_argument(arg):
        """
        Create a decorator which will pass the given argument as the nth
        argument of the wrapped function, where n has been supplied during this
        function's construction.
        """
        arg_tuple = (arg,)
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*(args[:arg_n] + arg_tuple + args[arg_n:]), **kwargs)
            return wrapper
        return decorator
    return nth_argument

first_argument = nth_argument_factory(0)
second_argument = nth_argument_factory(1)


def scale_float(value, x_min, x_max):
    return float(value) * (x_max - x_min) + x_min
