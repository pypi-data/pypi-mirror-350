from functools import wraps
from vcgImageAI.comm.contextManagers import ExceptionCatcher
from loguru import logger as logger


def HelloA():
    def real(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info("helloA started")
            # raise Exception("sdfsdfsd")

            response = func(*args, **kwargs)
            logger.info("helloA ended")

            return response

        return wrapper

    return real


def HelloB():
    def real(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info("helloB started")

            raise Exception("sdfsdfsd")

            response = func(*args, **kwargs)
            logger.info("helloB ended")

            return response

        return wrapper

    return real


class A(object):
    def __init__(self) -> None:
        pass

    @HelloA()
    @HelloB()
    def run(self):
        with ExceptionCatcher() as ec:
            logger.info("this is a test")
            logger.info("run")


if __name__ == "__main__":
    a = A()
    a.run()
