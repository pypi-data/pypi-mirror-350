import os
import sys
from pathlib import Path

from loguru import logger as logger1

from souJpg.comm.cfg.utils import initGcf
from souJpg.comm.contextManagers import ExceptionCatcher

gcfFilePath = os.getenv("gcfFilePath", None)
gcf = None
with ExceptionCatcher() as ec:
    if gcfFilePath is None:
        logger1.error("gcfFilePath is not set")
        raise Exception("gcfFilePath is not set")

    gcf = initGcf(baseConf=gcfFilePath)
if ec.error:
    logger1.error(f"Failed to load gcf: {ec.error}")
