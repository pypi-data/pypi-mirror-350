import logging
import os
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass


class GameLoggerAdapter(logging.LoggerAdapter):
    """Adapter that adds game character context to log messages."""
    
    def __init__(self, logger, char="Root"):
        super().__init__(logger, {"char": char})
        self.char = char
        self.DEBUG: int = logging.DEBUG
        self.INFO: int = logging.INFO
        self.WARNING: int = logging.WARNING
        self.ERROR: int = logging.ERROR
        self.CRITICAL: int = logging.CRITICAL

    def process(self, msg, kwargs):
        kwargs.setdefault("extra", {}).update(self.extra)
        return msg, kwargs
    
    def debug(self, msg: str, src: str = None) -> None:
        if src:
            self.extra["char"] = src
        super().debug(msg)
        if src:
            self.extra["char"] = self.char
    
    def info(self, msg: str, src: str = None) -> None:
        if src:
            self.extra["char"] = src
        super().info(msg)
        if src:
            self.extra["char"] = self.char
    
    def warning(self, msg: str, src: str = None) -> None:
        if src:
            self.extra["char"] = src
        super().warning(msg)
        if src:
            self.extra["char"] = self.char
    
    def error(self, msg: str, src: str = None) -> None:
        if src:
            self.extra["char"] = src
        super().error(msg)
        if src:
            self.extra["char"] = self.char
    
    def critical(self, msg: str, src: str = None) -> None:
        if src:
            self.extra["char"] = src
        super().critical(msg)
        if src:
            self.extra["char"] = self.char


def setup_game_logger(name: str = __name__):
    """Setup and return a GameLoggerAdapter instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Console handler with colored output
    console_formatter = logging.Formatter(
        fmt="\33[34m[%(levelname)s] %(asctime)s - %(char)s:\33[0m %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    
    # File handler with detailed output
    file_formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s - %(char)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = RotatingFileHandler(
        filename=f'logs/game_{datetime.now().strftime("%Y%m%d")}.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Add handlers if they haven't been added already
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return GameLoggerAdapter(logger)


# Initialize logger
logger = setup_game_logger()