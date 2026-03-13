import logging
import os

from logging.handlers import TimedRotatingFileHandler

class Logger:

    LOG_DIR = "logs"
    LOG_FILE = "logs/app.log"

    @classmethod
    def get_logger(cls, name="app_logger", level=logging.INFO):

        if not os.path.exists(cls.LOG_DIR):
            os.makedirs(cls.LOG_DIR)

        logger = logging.getLogger(name)

        if logger.handlers:
            return logger

        logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # Handler rotativo por dia
        file_handler = TimedRotatingFileHandler(
            cls.LOG_FILE,
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)
        file_handler.suffix = "%Y-%m-%d"

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger