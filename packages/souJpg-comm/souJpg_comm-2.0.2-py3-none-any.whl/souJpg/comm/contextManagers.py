from functools import wraps
import traceback
from typing import Optional

from loguru import logger as logger1

import time


class ExecuteTimeRecorder(object):
    """
    __exit__  return True,  if return false, program will exist
    if code block execute without any exceptions, error field will be None, others will be exception message
    """

    def __init__(self, identity=None) -> None:
        self.start_time = time.time()
        self.end_time = None
        self.identity = identity

    def __enter__(self):

        return self

    def __exit__(self, type, value, tb):
        self.end_time = time.time()
        logger1.info(
            "Execution time: {} seconds for {}",
            self.end_time - self.start_time,
            self.identity,
        )
        if value is not None:
            raise Exception(value)

        return True


class ExceptionCatcher(object):
    """
    __exit__  return True,  if return false, program will exist
    if code block execute without any exceptions, error field will be None, others will be exception message
    """

    def __init__(self) -> None:
        self.error = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        if value is not None:
            self.error = str(value)

            logger1.info("error: {}", value)
            logger1.debug(traceback.format_exc())
            logger1.debug(traceback.print_tb(tb))

        return True


def methodRetryWraper(maxAttempts=3):
    """
    only for method that raise Exception
    """

    def real(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            response = None
            ec = None
            while True:
                if attempts > maxAttempts:
                    raise Exception(ec.error)

                with ExceptionCatcher() as ec:
                    response = func(*args, **kwargs)

                if ec.error is None:
                    break
                else:
                    attempts += 1
                    logger1.info("retrying {} times", attempts)

            return response

        return wrapper


    return real

if __name__ == "__main__":
    with ExceptionCatcher() as ec:
        logger1.info("this is a test")
        raise Exception("sdfsdfsd")
    logger1.info(ec.error)
