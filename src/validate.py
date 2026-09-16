import logging

import pydantic

import pandas as pd

from types import MappingProxyType
from pydantic import ValidationError, TypeAdapter
from . import LOGGER_NAME, TemperatureRead


logger = logging.getLogger(LOGGER_NAME)

def _validate_temperature_records(data: list[dict], dataset_name: str) -> pd.DataFrame:
    processed_records = []
    flagged_count = 0

    for row in data:
        row_copy = row.copy()

        try:
            # Unpack the dictionary row as arguments to the Pydantic model to validate all fields.
            TemperatureRead(**row)
            row_copy["flagged_for_manuel_review"] = False

        except ValidationError as error:
            row_copy["flagged_for_manuel_review"] = True
            flagged_count += 1

        processed_records.append(row_copy)

    if flagged_count > 0:
        logger.warning(f"in {dataset_name}: {flagged_count} of {len(data)} rows were flagged for manual review.")
    else:
        logger.info(f"{dataset_name} had no flagged for manual review of {len(data)} rows.")

    return pd.DataFrame(processed_records)


def _validate_region(
    df: pd.DataFrame, 
    dataset_name: str, 
    known_region_mapping: dict | None = None
    ) -> pd.DataFrame:

    return None