""""""

import logging

from . import (
    LOGGER_NAME,
    configure_logging,
    MOCK_DATA_FOLDER,
    generate_mock_data,
    load_json_to_dataframe,
    auto_correct_regions,
    validate_temperature_records,
    save_csv
)

data_names = [
"correct_data",
"include_null_data",
"incorrect_data",
"mixed_failure_data",
"unit_incorrect_data",
]

def main() -> None:
    """Run packet"""

    #Configure logging for application.
    configure_logging()

    logger = logging.getLogger(LOGGER_NAME)
    logger.info("Sensor pipeline started from CLI (__main__).")

    #Create Mock data.

    generate_mock_data()

    #Load Mock data from .Json to DataFrame

    for data_name in data_names:

        df_mock = load_json_to_dataframe(file_path=f"{MOCK_DATA_FOLDER}/{data_name}.json")

        print(f"loaded mock data: {data_name}")
        #Auto correct common misspelling mistakes.
        auto_corrected_df_mock = auto_correct_regions(df_mock)

        print(f"Auto Corrected common misspelling for{df_mock}")

        #Validate using pydantic schema.
        validated_df_mock = validate_temperature_records(auto_corrected_df_mock, data_name)

        print(f"Validated using pydantic schema on {df_mock}")

        print(validated_df_mock)

        save_csv(data_name, validated_df_mock)
        print(f"saved {data_name} as CSV to folder output.")




if __name__ == "__main__":
    main() 