from funlogger import logger
from funlogger.config import config

config.LOG_FILE_PATH = "."
config.TAG = "agent"
logger = logger()

logger.info("xxx")
logger.debug("yyy")
logger.error("zzz")