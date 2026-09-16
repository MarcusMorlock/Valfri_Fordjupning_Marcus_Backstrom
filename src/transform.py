from types import MappingProxyType
import pandas as pd

# Read-only default mapping for character encoding and case errors.
KNOWN_REGION_MAPPINGS = MappingProxyType({
    "orebro": "Örebro",
    "sthlm": "Stockholm",
    "stockholms": "Stockholm",
})


def auto_correct_regions(
    df: pd.DataFrame, 
    mapping: dict | MappingProxyType | None = None
) -> pd.DataFrame:

    mapping_to_use = mapping if mapping is not None else KNOWN_REGION_MAPPINGS
    
    df_copy = df.copy()

    
    cleaned_series = df_copy["region"].astype(str).str.strip().str.lower()
    
    
    mapped_values = cleaned_series.map(mapping_to_use)
    
    
    has_match = mapped_values.notna()

    
    df_copy["original_region"] = df_copy["region"].where(has_match, df_copy.get("original_region", None))
    df_copy["auto_cleaned"] = has_match | df_copy.get("auto_cleaned", False)
    df_copy["region"] = mapped_values.fillna(df_copy["region"])

    return df_copy