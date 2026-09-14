import pydantic
import logging
import json

import pandas as pd

from pathlib import Path
from src import LOGGER_NAME, load_json, save_csv

#   {
#     "sensor_id": "S1",
#     "region": "Orebro",
#     "sector": "W",
#     "temperature": 20.0
#   },

