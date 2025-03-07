"""
This is the Classification Engine, responsible for handling and applying
the classification rules to the dataset.
"""

from __future__ import annotations

import json
import logging

import pandas as pd
from pandas import DataFrame

from src.exceptions import InvalidClassificationEngineException
from src.rules_engine import DynamicRulesEngine, StaticRulesEngine

logger = logging.getLogger(__name__)


class ClassificationEngine:
    """This class is responsible for handling different classification
    engines and being the interface with the orchestrator script.
    """

    def __init__(self):
        logger.info("Creating Dynamic Rules Engine...")
        self.rule_processor = DynamicRulesEngine()
        logger.info("Creating Static Rules Engine...")
        self.rules_engine = StaticRulesEngine()

    def _static_classification(self, company_data: pd.Series) -> dict:
        """
        Apply all static classification rules.

        :param company_data: A pandas Series with the company information.
        :return: A dictionary with the classification results.
        """
        company_description = company_data["Description"]
        founded_year = company_data["Founded Year"]
        headquarters = company_data["Headquarters"]
        total_employees = company_data["Total Employees"]
        employee_locations = json.loads(company_data["Employee Locations"])

        results = {
            "is_recent": self.rules_engine.is_founded_in_last_5_years(
                founded_year
            ),
            "is_saas": self.rules_engine.is_saas_company(company_description),
            "is_us_based": self.rules_engine.is_us_based(headquarters),
            "most_employees_are_us_based": self.rules_engine.most_of_employees_are_us_based(
                employee_locations
            ),
            "has_20_to_60_employees": self.rules_engine.has_20_to_60_employees(
                total_employees
            ),
        }

        is_interesting = all(results.values())
        return {"is_interesting": is_interesting, "rule_results": results}

    def _dynamic_classification(self, company_data: pd.Series) -> dict:
        """
        Apply all dynamic classification rules.

        :param company_data: A pandas Series with the company information.
        :return: A dictionary with the classification results.
        """
        rules_set = self.rule_processor.parse_rules()
        results = {}
        for rule in rules_set:
            evaluation = rule.apply_rule(company_data)
            results[rule.rule_id] = evaluation

        results["is_saas"] = StaticRulesEngine.is_saas_company(
            company_data["Description"]
        )

        is_interesting = all(results.values())
        return {"is_interesting": is_interesting, "rule_results": results}

    def classify(self, classification_engine, companies_df) -> DataFrame:
        """
        This method is the interface and is the entrypoint to the
        classification engine.

        :param classification_engine:
        :param companies_df:
        :return: A pandas DataFrame with columns indicating the overall
                evaluation based on the set of rules,
                and columns indicating the individual rule application result.
        """
        company_data: pd.Series
        results = []
        available_classifiers = {
            "static": self._static_classification,
            "dynamic": self._dynamic_classification,
        }
        engine = available_classifiers.get(classification_engine, None)
        if engine is None:
            raise InvalidClassificationEngineException(
                message=f"Unknown classification engine: {classification_engine}"
            )
        for _, company_data in companies_df.iterrows():
            classification = engine(company_data)
            results.append(
                {
                    **company_data.to_dict(),
                    "is_interesting": classification["is_interesting"],
                    **classification["rule_results"],
                }
            )
        return pd.DataFrame(results)
