import logging
import os
from pathlib import Path


def getLogger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    def enable_pretty_logging():
        if not logger.handlers:
            # Configure handler
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)1s][%(asctime)s %(module)s:%(lineno)d pid:%(process)d] %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False

    enable_pretty_logging()
    return logger


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class TimeStamp:
    time_stamp = None

    def getTimeStamp(cls):
        if cls.time_stamp is None:
            import datetime
            cls.time_stamp = datetime.datetime.now().strftime('%Y%m%d%H_%M%S%f')
        return cls.time_stamp


from uiautomator2 import Device
d = Device


def getProjectRoot():
    root = Path("/")
    cur_dir = Path.absolute(Path(os.curdir))
    while not os.path.isdir(cur_dir / "configs"):
        if cur_dir == root:
            return None
        cur_dir = cur_dir.parent
    return cur_dir