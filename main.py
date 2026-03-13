from core import logger
from core.config import Config
from core.logger import Logger

logger = Logger.get_logger(__name__)

def start():

    Config.validate()

    logger.info("Application started")

if __name__ == "__main__":
    start()