from .logger import logger, LoggerConfigurator, LoggerLevel

configurator = LoggerConfigurator()

__all__ = [
    "logger",
    "configurator",
    "LoggerLevel"
]
