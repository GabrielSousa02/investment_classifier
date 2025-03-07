import logging
import time

import pandas as pd

from src.exceptions import EmptyDatasetException
from src.utils.data_utils import sanitize_dataframe

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, sanitizing_strategy: int):
        self.sanitizing_strategy = sanitizing_strategy

    def load_companies(self, file_path):
        """
        Load company data from CSV
            - Validate data integrity
            - Handle missing values

        :param file_path: The file path for the dataset.
        :return: A Pandas DataFrame
        """
        try:
            logger.info(f"Loading companies from {file_path}...")
            df = pd.read_csv(file_path)
            if len(df) == 0:
                raise EmptyDatasetException(
                    message="Cannot load empty dataset"
                )
            # Sanitize the DF
            start_time = time.time()
            logger.info("Sanitizing the DataFrame...")
            logger.info(f"Sanitizing strategy {self.sanitizing_strategy}...")
            sanitized_df = sanitize_dataframe(df, self.sanitizing_strategy)
            # Get final timer and calculate duration
            ending_time = time.time()
            duration = ending_time - start_time
            logger.info("Sanitizing process concluded!")
            logger.info(f"Sanitizing process duration: {duration:.2f}")

            return sanitized_df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
