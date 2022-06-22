import logging

logger = logging.getLogger("pylox")
logger.setLevel(logging.DEBUG)
BASE_FORMAT = (
    "[%(levelname)-6s][%(name)s.%(filename)s:%(lineno)d][%(funcName)10s] %(message)s"
)

file_logger = logging.FileHandler("pylox.log")
file_logger.setLevel(logging.DEBUG)
file_logger.setFormatter(logging.Formatter(BASE_FORMAT))

logger.addHandler(file_logger)
