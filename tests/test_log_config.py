"""Log configure testing."""

import logging
import pytest

from pathlib import Path

from src.log_config import LOGGER_NAME, configure_logging

@pytest.fixture(autouse=True)
def cleanup_logger():
    """Clean RAM after opening filhantag before and after each test."""
    logger = logging.getLogger(LOGGER_NAME)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()
    yield
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()


def test_configure_logging_creates_directory_and_file(tmp_path: Path):

    test_log_file = tmp_path / "custom_logs" / "test.log"
    configure_logging(log_path=test_log_file)

    assert test_log_file.parent.exists()
    assert test_log_file.exists()


def test_configure_logging_prevent_duplicate_handlers(tmp_path: Path):

    test_log_file = tmp_path / "test.log"
    logger = logging.getLogger(LOGGER_NAME)

    # Run twice to reveal any duplicates.
    configure_logging(log_path=test_log_file)
    configure_logging(log_path=test_log_file)

    # Count exactly the types of handlers you add yourself (excluding Pytest's LogCaptureHandler).
    file_handlers = [h for h in logger.handlers if type(h) is logging.FileHandler]
    stream_handlers = [h for h in logger.handlers if type(h) is logging.StreamHandler]

    assert len(file_handlers) == 1
    assert len(stream_handlers) == 1


def test_logging_writes_to_file(tmp_path: Path):

    #Create temp file and path     
    test_log_file = tmp_path / "test.log"
    configure_logging(log_path=test_log_file)

    logger = logging.getLogger(LOGGER_NAME)
    logger.debug("Test debug message")
    logger.info("Test info message")

    # Force a write and close the file so the disk is fully updated.
    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()

    content = test_log_file.read_text(encoding="utf-8")
    assert "Test debug message" in content
    assert "Test info message" in content