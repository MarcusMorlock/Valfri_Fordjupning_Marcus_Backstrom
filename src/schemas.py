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


class TemperatureRead(BaseModel):
    sensor_id: str = Field(min_length=2)
    region: str = Field(min_length=1)
    sector: SectorType
    # Temperatures above 40.0 °C are immediately rejected as implausible/Fahrenheit/sensor errors/ input error. and below -50.0 °C as implausible/sensor errors/input error.
    temperature: float = Field(ge=-50.0, le=40.0)

    @field_validator("region")
    @classmethod
    def validate_region_not_junk(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if cleaned in ["none", "null", "n/a", "", "unknown"]:
            raise ValueError(f"Invalid region placeholder: '{value}'")
        return value