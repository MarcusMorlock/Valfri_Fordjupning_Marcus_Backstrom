from types import MappingProxyType
import pandas as pd
import logging

from . import LOGGER_NAME

# Read-only default mapping for character encoding and case errors.
KNOWN_REGION_MAPPINGS = MappingProxyType({
    "orebro": "Örebro",
    "sthlm": "Stockholm",
    "stockholms": "Stockholm",
})

logger = logging.getLogger(LOGGER_NAME)

def auto_correct_regions(
    df: pd.DataFrame, 
    mapping: dict | MappingProxyType | None = None
) -> pd.DataFrame:

    mapping_to_use = mapping if mapping is not None else KNOWN_REGION_MAPPINGS
    
    df_copy = df.copy()

    #Check if dataframe contain "region"
    if "region" not in df_copy.columns:
        raise ValueError(f"DataFrame did not contain column: region")

    #add column if it does not exist
    if "original_region" not in df_copy.columns:
        df_copy["original_region"] = None
    if "auto_cleaned" not in df_copy.columns:
        df_copy["auto_cleaned"] = False

    #Clean from white space and lower and upper cases from the mapping list
    safe_mapping = {
        str(k).strip().lower(): str(v).strip().title() 
        for k, v in mapping_to_use.items()
        }

    #take out region and remove whitespace from the dataframe in column "region" and make it lower
    lookup_keys = df_copy["region"].astype(str).str.strip().str.lower()

    #check the regions inside lookup_keys against the mapped list where it return the mapped value if matched otherwise NaN.
    mapped = lookup_keys.map(safe_mapping)

    # Identify which rows are actually changing (present in the mapping AND different from the current region)
    actually_changed = mapped.notna() & (mapped != df_copy["region"])

    #Set True or False for which "original_region" should be saved and is currently empty so it does not overide preexisting data. 
    needs_original_saved = actually_changed & df_copy["original_region"].isna()

    #Check needs_original_saved and if it´s true then "original_region" will have the current unchanged "region" saved in to keep records.
    df_copy.loc[needs_original_saved, "original_region"] = df_copy.loc[needs_original_saved, "region"]

    #uses loc and if actually_changed is true auto_cleaned will be set to True
    df_copy.loc[actually_changed, "auto_cleaned"] = True

    #uses loc and if actually_changed is true set the dataframe´s "region" to the mapped indexed value.
    df_copy.loc[actually_changed, "region"] = mapped[actually_changed]

    #write to log the amount autocorrected for logging purposes
    corrected_count = int(actually_changed.sum())
    if corrected_count > 0:
        logger.info(f"Auto-corrected {corrected_count} region entries.")
    else:
        logger.info("No regions required auto-correction.")

    return df_copy