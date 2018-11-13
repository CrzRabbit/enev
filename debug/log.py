from enum import Enum
import logging; logging.basicConfig(level=logging.INFO)

currentlevel = 2

class logcf(Enum):
    base = 0
    database = 1
    controller = 2
    modle = 3
    message = 4

logconf = (logcf.base, )

def logi(logcf, info):
    if logconf.__contains__(logcf):
        logging.info(info)

def loge(logcf, info):
    if logconf.__contains__(logcf):
        logging.error(info)

def logw(logcf, info):
    if logconf.__contains__(logcf):
        logging.warning(info)

def logd(logcf, info):
    if logconf.__contains__(logcf):
        logging.debug(info)