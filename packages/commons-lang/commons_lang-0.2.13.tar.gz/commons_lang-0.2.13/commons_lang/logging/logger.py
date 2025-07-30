import logging
import sys
from typing import Union
from enum import Enum

from loguru import logger


class LoggerLevel(Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggerConfigurator:

    def __init__(self):
        self.logger = logger
        self.raw_package_levels = {}
        self.new_package_levels = {}
        self.set_up_base_logger()

    def set_up_base_logger(self):
        self.logger.remove()

        def dynamic_filter(record) -> bool:
            name = record["name"]
            for package_name, min_level in self.new_package_levels.items():
                if name.startswith(package_name):
                    if record["level"].no < min_level.no:
                        return False
            return True

        colorful_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<level>{message}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
        )

        self.logger.add(
            sys.stdout,
            format=colorful_format,
            level="TRACE",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            filter=dynamic_filter
        )

    def set_package_level(self, package_name: str, level: Union[str, LoggerLevel]):
        level = level.value if isinstance(level, LoggerLevel) else level

        if package_name not in self.raw_package_levels:
            raw_logger = logging.getLogger(package_name)
            self.raw_package_levels[package_name] = raw_logger.level

            if self.raw_package_levels[package_name] == logging.NOTSET:
                self.raw_package_levels[package_name] = raw_logger.getEffectiveLevel()

        self.new_package_levels[package_name] = logger.level(level)
        logging.getLogger(package_name).setLevel(getattr(logging, level))

    def reset_package_level(self, package_name: str):
        if package_name in self.new_package_levels:
            del self.new_package_levels[package_name]

            if package_name in self.raw_package_levels:
                raw_level = self.raw_package_levels[package_name]
                logging.getLogger(package_name).setLevel(raw_level)
                del self.raw_package_levels[package_name]
