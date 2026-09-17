import json
import logging


from pathlib import Path
from . import LOGGER_NAME

import pandas as pd


logger = logging.getLogger(LOGGER_NAME)

def load_json_to_dataframe(file_path: Path) -> pd.DataFrame:
    """Load JSON file from file_path."""

    file_path = Path(file_path)

    if not file_path.exists():
        logger.error(f"File could not be found: {file_path}")
        raise FileNotFoundError(f"Could not find file {file_path}")

    try:

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Successfully read JSON file at: {file_path}")
        if isinstance(data, dict):
            data = [data]

        return pd.DataFrame(data)

    except json.JSONDecodeError as error:
        logger.error(f"Failed to read JSON file at {file_path}: {error}")
        raise ValueError(f"Could not read file as JSON: {file_path}") from error

def save_csv (file_name: str, df: pd.DataFrame) -> None:

    if not file_name.endswith(".csv"):
        file_name = f"{file_name}.csv"

    clean_name = Path(file_name).name  
    _output_path = Path("output") / clean_name

    _output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        df.to_csv(_output_path, index=False, encoding="utf-8")
        logger.info(f"Saved {len(df)} rows to: {_output_path}")

    except OSError as error:
        logger.error(f"Failed to write CSV file at: {_output_path}: {error}")
        raise IOError(f"Could not write CSV file: {_output_path}") from error