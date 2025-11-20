import os
import logging
from logging import StreamHandler, FileHandler, Formatter
from datetime import date
from pathlib import Path

class Logger:
    def __init__(self, file_name: str) -> None:
        today = date.today().strftime("%Y_%m_%d")
        if file_name.lower().endswith(".log"):
            file_name = file_name[:-4]
        logs_dir = "logs"
        Path(logs_dir).mkdir(exist_ok=True, parents=True)
        self.file_name = os.path.join(logs_dir, f"{file_name}_{today}.log")

        self.logger = logging.getLogger(self.file_name)
        self.logger.setLevel(level=logging.DEBUG)

        formatter = Formatter(
            "{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M"
        )

        console_handler = StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        file_handler = FileHandler(
            filename=self.file_name,
            mode="a",
            encoding="utf8",
        )
        # file_handler.setLevel(level=logging.WARNING)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)

