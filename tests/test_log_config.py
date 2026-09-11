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

    # Körs två gånger för att framkalla ev. dubletter
    configure_logging(log_path=test_log_file)
    configure_logging(log_path=test_log_file)

    # Räkna exakt de typer av handlers du själv lägger till (exkludera Pytests LogCaptureHandler)
    file_handlers = [h for h in logger.handlers if type(h) is logging.FileHandler]
    stream_handlers = [h for h in logger.handlers if type(h) is logging.StreamHandler]

    assert len(file_handlers) == 1
    assert len(stream_handlers) == 1


def test_logging_writes_to_file(tmp_path: Path):
    test_log_file = tmp_path / "test.log"
    configure_logging(log_path=test_log_file)

    logger = logging.getLogger(LOGGER_NAME)
    logger.debug("Test debug message")
    logger.info("Test info message")

    # Tvinga skrivning och stäng filen så disken uppdateras helt
    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()

    content = test_log_file.read_text(encoding="utf-8")
    assert "Test debug message" in content
    assert "Test info message" in content