import json

from pathlib import Path

MOCK_DATA_FOLDER = "data"

def generate_mock_data() -> None:
    correct_data = [
        {"sensor_id": "S1", "region": "Örebro", "sector": "W", "temperature": 20.0},
        {"sensor_id": "S2", "region": "Örebro", "sector": "C", "temperature": 21.2},
        {"sensor_id": "S3", "region": "Örebro", "sector": "SE", "temperature": 20.3},
        {"sensor_id": "S4", "region": "Örebro", "sector": "S", "temperature": 20.5},
        {"sensor_id": "S5", "region": "Stockholm", "sector": "C", "temperature": 10.0}
    ]

    incorrect_data = [
        {"sensor_id": "S1", "region": "Örebro", "sector": "väster", "temperature": 20.0},
        {"sensor_id": "S2", "region": "Orebro", "sector": "Centrum", "temperature": 21.2},
        {"sensor_id": "S3", "region": "orobro", "sector": "SE", "temperature": 20.3},
        {"sensor_id": "S4", "region": "Orebro", "sector": "S", "temperature": 20.5},
        {"sensor_id": "S5", "region": "Stockish", "sector": "Centrum", "temperature": 10.0}
    ]

    include_null_data = [
        {"sensor_id": "S1", "region": "None", "sector": "W", "temperature": 20.0},
        {"sensor_id": "S2", "region": "", "sector": "C", "temperature": 21.2},
        {"sensor_id": "S3", "region": "Orebro", "sector": "SE", "temperature": None},
        {"sensor_id": "S4", "region": "Orebro", "sector": "", "temperature": 20.5},
        {"sensor_id": "S5", "region": "Stockholm", "sector": "C", "temperature": 10.0}
    ]

    unit_incorrect_data = [
        {"sensor_id": "S1", "region": "Orebro", "sector": "W", "temperature": 30.0},
        {"sensor_id": "S2", "region": "Orebro", "sector": "C", "temperature": 21.2},
        {"sensor_id": "S3", "region": "Orebro", "sector": "SE", "temperature": 50.3},
        {"sensor_id": "S4", "region": "Orebro", "sector": "S", "temperature": 20.5},
        {"sensor_id": "S5", "region": "Stockholm", "sector": "C", "temperature": 100.0}
    ]

    mixed_failure_data = [
        {"sensor_id": "S1", "region": "Örebro", "sector": "West", "temperature": 20.0},
        {"sensor_id": "S2", "region": "Orebro", "sector": "C", "temperature": 51.2},
        {"sensor_id": "S3", "region": "orobo", "sector": "SE", "temperature": 20.3},
        {"sensor_id": "S4", "region": "Orebro", "sector": "Söder", "temperature": 30.5},
        {"sensor_id": "S5", "region": "Stockholm", "sector": "C", "temperature": 10.0}
    ]

    # 
    datasets = {
        "correct_data.json": correct_data,
        "incorrect_data.json": incorrect_data,
        "include_null_data.json": include_null_data,
        "unit_incorrect_data.json": unit_incorrect_data,
        "mixed_failure_data.json": mixed_failure_data
    }

    data_dir = Path(MOCK_DATA_FOLDER)
    data_dir.mkdir(exist_ok=True)


    # Create mock data inside folder data
    for filename, data in datasets.items():
        filepath = data_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


    print(f"Saved {len(datasets)} mock data json files to {data_dir}/")