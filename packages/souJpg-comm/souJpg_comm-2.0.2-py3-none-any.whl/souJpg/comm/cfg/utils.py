import ast
import json
import os
from pathlib import Path

from omegaconf import DictConfig, ListConfig, OmegaConf
from loguru import logger as logger1

# envVariablesSupportedList = [
#     "newAddedImageQueueName",
#     "asyncUserRequestsTableName",
#     "syncUserRequestsTableName",
# ]


def convert_string_to_type(value, data_type):
    """
    Convert a string to a specified data type.
    :param value: The string to be converted.
    :param data_type: The data type to convert the string to.
    :return: The converted value.
    """
    if data_type == int:
        return int(value)
    elif data_type == float:
        return float(value)
    elif data_type == bool:
        return ast.literal_eval(value.capitalize())
    elif data_type == str:
        return str(value)
    elif data_type == DictConfig:
        return json.loads(value)
    elif data_type == ListConfig:
        return ast.literal_eval(value)
    else:
        raise Exception(f"Unsupported data type: {data_type}")


def initGcf(baseConf=None):
    # check if user specify a config file, if yes, then merge it with baseConf.yaml
    gcf = None
    baseGcf = OmegaConf.load(baseConf)
    userConf = "/etc/imageFrontApi/conf.yaml"
    userConfPath = Path(userConf)
    if userConfPath.is_file():
        userGcf = OmegaConf.load(userConf)
        gcf = OmegaConf.merge(baseGcf, userGcf)
    else:
        gcf = baseGcf
    for key in gcf:
        valueType = type(gcf[key])

        envValue = os.getenv(key)
        if envValue is not None and envValue != "":
            envValue = convert_string_to_type(envValue, valueType)

            gcf[key] = envValue
    logger1.info(f"gcf: {gcf}")

    return gcf


def initErrorCodeMap(baseConf=None):
    # check if user specify a config file, if yes, then merge it with baseConf.yaml
    gcf = None
    baseGcf = OmegaConf.load(baseConf)
    userConf = "/etc/imageFrontApi/errorCodes_zh.yaml"
    userConfPath = Path(userConf)
    if userConfPath.is_file():
        userGcf = OmegaConf.load(userConf)
        gcf = OmegaConf.merge(baseGcf, userGcf)
    else:
        gcf = baseGcf

    return gcf
