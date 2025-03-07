"""
Main file/entry point to orchestrate the Investment Company Classifier.
"""

import logging
import time
from datetime import datetime
from pathlib import Path

from src.classifier import ClassificationEngine
from src.config import config
from src.data_loader import DataLoader


def main():
    # Instantiate logger for this file/module
    logger = logging.getLogger(__name__)

    # Start function initial timer
    start_time = time.time()

    # Get configuration params
    logger.info("Loading configuration data...")

    data_sanitizing_strategy = config.get(
        "application.data_sanitizing_strategy"
    )

    classification_engine = (
        config.get("application.classification_engine") or "static"
    )

    base_dir = str(Path(__file__).cwd()) + "/"
    input_base_path = base_dir + config.get(
        "data_sources.input_base_path", "data/input/"
    )
    output_base_path = base_dir + config.get(
        "data_sources.output_base_path", "data/output/"
    )
    input_filename = config.get("data_sources.input_filename")

    # Load data
    logger.info("Loading dataset...")
    logger.info(f"Dataset name: {input_filename}...")
    data_loader = DataLoader(data_sanitizing_strategy)
    companies_df = data_loader.load_companies(
        f"{input_base_path}{input_filename}"
    )

    # Initialize classifier
    logger.info("Creating Classifier engine...")
    classifier = ClassificationEngine()

    # Classify companies
    logger.info("Classification initiated...")
    logger.info(f"Engine selected: {classification_engine}")
    results_df = classifier.classify(classification_engine, companies_df)

    # Convert to DataFrame and save
    logger.info("Classification completed...")
    logger.info("Saving results...")
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
