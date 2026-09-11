"""Configure logging for project."""

import logging

from pathlib import Path

LOGGER_NAME = "temperature_log"

def configure_logging(log_path: Path = Path("logs/temperature.log")) -> None:
    logger = logging.getLogger(LOGGER_NAME)

    log_path = Path(log_path)

    if any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        return

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(
        log_path,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)