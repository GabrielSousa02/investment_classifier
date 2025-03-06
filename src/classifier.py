"""
This is the Classification Engine, responsible for handling and applying
the classification rules to the dataset.
"""

import json
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class ClassificationEngine:
    def __init__(self, rules_engine):
        # self.rules = rule_set
        # self.rule_aggregator = RuleAggregator()
        # self.rule_processor = RuleProcessor(rule_set)
        self.rules_engine = rules_engine

    def classify_company(self, company_data):
        """Apply all classification rules
        Return classification result with reasoning
        """
        company_description = company_data["Description"]
        founded_year = company_data["Founded Year"]
        headquarters = company_data["Headquarters"]
        employee_locations = json.loads(company_data["Employee Locations"])

        if type(company_description) is float:
            company_description = company_data["Company Name"]

        if founded_year is None:
            founded_year = datetime.now().year

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
                employee_locations
            ),
        }

        # Determine final classification
        is_interesting = all(results.values())
        return {"is_interesting": is_interesting, "rule_results": results}

        # PROCESS EACH DYNAMIC RULE
        # rule_results = [
        #     self.rule_processor.process_rule(rule, company_data)
        #     for rule in self.rules
        # ]

        # Aggregate results
        # classification_score = self.rule_aggregator.aggregate(rule_results)

        # Determine final classification
        # return self._make_decision(classification_score, rule_results)

    def _make_decision(self, score, rule_results, company_data):
        # Complex decision-making logic
        # Check critical rules
        # Consider overall score
        # Provide detailed reasoning

        # Rule 1: Founded in past 5 years
        founding_year = company_data["founding_year"]
        current_year = datetime.now().year
        is_recent_company = (current_year - founding_year) <= 5

        # Rule 2: Exact employee count
        employee_count = company_data["total_employees"]
        has_right_employee_count = employee_count == 2060

        # Rule 3: Location check
        headquarters_location = company_data["headquarters_location"]
        is_north_american = headquarters_location in ["USA", "Canada"]

        # Combine rules - all must be true
        is_interesting = (
            is_recent_company
            and has_right_employee_count
            and is_north_american
        )

        return "Interesting" if is_interesting else "Not Interesting"
