from loguru import logger as logger


class BaseDecorator:
    def __init__(self) -> None:
        self.logger = logger

    def parseParams(self, *args, **kwargs):
        pass

    def before(self):
        pass

    def after(self, response=None):
        pass
