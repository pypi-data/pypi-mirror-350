from functools import wraps

from loguru import logger as logger

from souJpg.comm.contextManagers import ExceptionCatcher


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
                    logger.info("retrying {} times", attempts)

            return response

        return wrapper

    # """
    # only for method that return BaseResponse
    # """

    # def real(func):
    #     @wraps(func)
    #     def wrapper(*args, **kwargs):
    #         attempts = 0
    #         response = None
    #         while True:

    #             if attempts > maxAttempts:

    #                 break
    #             response = func(*args, **kwargs)
    #             if (
    #                 response is None
    #                 or issubclass(type(response), BaseResponse) is False
    #             ):
    #                 logger.warning("this method not support retry")
    #                 break
    #             if response.error is None and response.errorCode is None:
    #                 break
    #             else:
    #                 attempts += 1
    #                 logger.info("retrying {} times", attempts)

    #         return response

    #     return wrapper

    return real
