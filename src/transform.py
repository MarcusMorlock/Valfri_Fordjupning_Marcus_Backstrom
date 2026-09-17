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

    if "region" not in df_copy.columns:
        return df_copy

    if "original_region" not in df_copy.columns:
        df_copy["original_region"] = None
    if "auto_cleaned" not in df_copy.columns:
        df_copy["auto_cleaned"] = False
    
    safe_mapping =  {
        str(k).strip().lower(): str(v).strip().title()
        for k, v in mapping_to_use.items()
    }
    
    safe_mapping = {str(k).strip().lower(): str(v).strip() for k, v in mapping_to_use.items()}

    
    lookup_keys = df_copy["region"].astype(str).str.strip().str.lower()
    mapped = lookup_keys.map(safe_mapping)

    
    has_match = mapped.notna()

    df_copy.loc[has_match, "original_region"] = df_copy.loc[has_match, "region"]
    df_copy.loc[has_match, "auto_cleaned"] = True
    df_copy.loc[has_match, "region"] = mapped[has_match]

    corrected_count = int(has_match.sum())
    if corrected_count > 0:
        logger.info(f"Auto-corrected {corrected_count} region entries.")
    else:
        logger.info("No regions required auto-correction.")

    return df_copy