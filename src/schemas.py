from typing import Literal
from pydantic import BaseModel, Field, field_validator

# Accepted Sectors
SectorType = Literal[
    "North", "N",
    "South", "S",
    "East", "E",
    "West", "W",
    "North-East", "NE",
    "North-West", "NW",
    "South-East", "SE",
    "South-West", "SW",
    "Centrum", "C"
]

ALLOWED_REGIONS = {"Örebro", "Stockholm", "Göteborg", "Malmö"}

class TemperatureRead(BaseModel):
    sensor_id: str = Field(min_length=2)
    region: str = Field(min_length=2,max_length=15)
    sector: SectorType
    temperature: float = Field(ge=-40.0, le=40.0)

    @field_validator("region")
    @classmethod
    def validate_region(cls, value: str) -> str:
        cleaned = value.strip().lower()

        if cleaned in ["none", "null", "n/a", "", "unknown", "nan", "undefined"]:
            raise ValueError(f"Invalid region placeholder: '{value}'")


        if value not in ALLOWED_REGIONS:
            raise ValueError(
                f"Unrecognized region '{value}'. Flagged for manual review."
            )

        return value