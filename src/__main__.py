""""""

import logging

from .log_config import (
    LOGGER_NAME,
    configure_logging
)

def main() -> None:
    """Run packet"""

    configure_logging()

    logger = logging.getLogger(LOGGER_NAME)
    logger.info("Sensor pipeline started from CLI (__main__).")

    print("Pipeline initialized. Ready for data processing.")

if __name__ == "__main__":
    main() 