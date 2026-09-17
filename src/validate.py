import logging

import pydantic

import pandas as pd

from types import MappingProxyType
from pydantic import ValidationError, TypeAdapter
from . import LOGGER_NAME, TemperatureRead
from .transform import auto_correct_regions


logger = logging.getLogger(LOGGER_NAME)

def validate_temperature_records(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    df_copy = df.copy()
    
    records = df_copy.to_dict(orient="records")
    flags = []

   
    for row in records:
        try:
            TemperatureRead(**row)
            flags.append(False)  
        except ValidationError:
            flags.append(True)   

    
    df_copy["flagged_for_manual_review"] = flags
    flagged_count = sum(flags)

    
    if flagged_count > 0:
        logger.warning(f"in {dataset_name}: {flagged_count} of {len(df_copy)} rows were flagged for manual review.")
    else:
        logger.info(f"{dataset_name} had no flagged for manual review of {len(df_copy)} rows.")

    return df_copy