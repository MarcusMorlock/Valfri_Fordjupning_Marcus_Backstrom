import logging


import pandas as pd

from pydantic import ValidationError
from . import LOGGER_NAME, TemperatureRead



logger = logging.getLogger(LOGGER_NAME)

def validate_temperature_records(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    df_copy = df.copy()
    
    # Gör om Pandas NaN till None
    clean_records = df_copy.where(pd.notnull(df_copy), None).to_dict(orient="records")
    flags = []

    for row in clean_records:
        try:
            TemperatureRead(**row)
            flags.append(False)  # Pass no flagging
        except ValidationError:
            flags.append(True)   # Flagged for manual review

    # Set true or false depending on the for loop above.
    df_copy["flagged_for_manual_review"] = flags
    flagged_count = sum(flags)

    #Write into log which dataset and how many rows were flagged for tracking.
    if flagged_count > 0:
        logger.warning(f"In {dataset_name}: {flagged_count} of {len(df_copy)} rows were flagged for manual review.")
    else:
        logger.info(f"{dataset_name} had no flagged rows out of {len(df_copy)} rows.")

    return df_copy