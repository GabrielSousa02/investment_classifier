"""
Main file/entry point to orchestrate the Investment Company Classifier.
"""

import logging
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.classifier import ClassificationEngine
from src.config import config
from src.data_loader import DataLoader
from src.rules_engine import StaticRulesEngine


def main():
    # Instantiate logger for this file/module
    logger = logging.getLogger(__name__)

    # Start function initial timer
    start_time = time.time()

    # Get configuration params
    logger.info("Loading configuration data...")
    base_dir = str(Path(__file__).cwd()) + "/"
    input_base_path = base_dir + config.get("data_sources.input_base_path")
    output_base_path = base_dir + config.get("data_sources.output_base_path")
    input_filename = config.get("data_sources.input_filename")

    # Load data
    logger.info("Loading dataset...")
    logger.info(f"Dataset name: {input_filename}...")
    data_loader = DataLoader()
    companies_df = data_loader.load_companies(
        f"{input_base_path}{input_filename}"
    )

    # Initialize classifier
    logger.info("Creating Rules engine...")
    rules_engine = StaticRulesEngine()
    logger.info("Creating Classifier engine...")
    classifier = ClassificationEngine(rules_engine)

    # Classify companies
    logger.info("Classification initiated...")
    results = []
    for _, company in companies_df.iterrows():
        classification = classifier.classify_company(company)
        results.append(
            {
                **company.to_dict(),
                "is_interesting": classification["is_interesting"],
            }
        )

    # Convert to DataFrame and save
    logger.info("Classification completed...")
    logger.info("Saving results...")
    results_df = pd.DataFrame(results)
    filename = (
        "parsed"
        + "_"
        + datetime.now().strftime("%Y%m%d-%H%M%S")
        + "_"
        + input_filename
    )

    # Get final timer and calculate duration
    ending_time = time.time()
    duration = ending_time - start_time

    results_df.to_csv(f"{output_base_path}{filename}", index=False)
    logger.info("Process completed!")
    logger.info(f"File created: {filename}")
    logger.info(f"Classification process duration: {duration:.2f}")


if __name__ == "__main__":
    main()
