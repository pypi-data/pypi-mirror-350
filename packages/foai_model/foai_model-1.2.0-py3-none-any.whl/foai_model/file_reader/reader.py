from pathlib import Path
import os
import pandas as pd
from foai_model.logger import logger

DATASETS_PATH = Path("data/datasets")


def read_datasets():
    all_dataframes = []
    expected_columns = ["Category", "Resume"]

    for filename in os.listdir(DATASETS_PATH):
        if filename.endswith(".csv"):
            path = os.path.join(DATASETS_PATH, filename)
            df = pd.read_csv(path)

            logger.info("Loaded file: %s", filename)
            logger.info("Dataset shape: %s", df.shape)

            if list(df.columns) != expected_columns:
                logger.warning(
                    "File '%s' has different columns and will be skipped.", filename
                )
                logger.warning("Expected columns: %d", expected_columns)
                logger.warning("Found columns: %s", list(df.columns))
                continue

            all_dataframes.append(df)

    if all_dataframes:
        final_dataset = pd.concat(all_dataframes, ignore_index=True)
        logger.info("Combined dataset shape: %s", final_dataset.shape)
    else:
        logger.warning("No CSV files with matching columns were loaded.")

    return final_dataset
