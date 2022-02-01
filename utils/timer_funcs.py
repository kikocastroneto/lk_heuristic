import time
import logging
from functools import wraps

# create the logger for the module
logger = logging.getLogger(__name__)


def improve_timer_decorator(improve_func):
    """
    A decorator to be used to report the time to perform the improvement loop

    :param improve_func: the improvement function to be decorated
    :type improve_func: function
    """

    # the function wrapper
    @wraps(improve_func)
    def wrapper(*args, **kwargs):

        # set the start time
        start_time = time.time()

        # execute the function
        improve_func(*args, **kwargs)

        # log the ending result
        logger.info(f"Finished '{improve_func.__name__}' function with best cost '{args[0].tour.cost:.3f}' found in {time.time() - start_time:.3f} seconds")

    # returns the wrapper function
    return wrapper


def timeit(func):
    """
    a decorator to time a function (mostly used for debugging)

    :param func: the function to be timed
    :type func: function
    :return: the decorated func
    :rtype: func
    """
    @wraps(func)
    def new_func(*args, **kwargs):

        # start time
        start_time = time.time()

        # execute the function
        result = func(*args, **kwargs)

        # compute elapsed time
        elapsed_time = time.time() - start_time

        # log the ending result
        logger.info('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsed_time * 1_000)))

        # returns the result of the function
        return result

    # returns the wrapper function
    return new_func
