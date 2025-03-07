"""
Parses user defined processing logic.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from math import floor
from typing import List

import numpy as np

from src.exceptions import (
    InsufficientRulesException,
    InvalidOperationException,
)
from src.rules_file_parser import InvestorRulesManager
from src.utils.rules_utils import apply_operation


class Rule:
    def __init__(
        self,
        name: str,
        rule_id: str,
        rule_type: str,
        parameters: dict,
    ):
        self.rule_id = rule_id
        self.name = name
        self.rule_type = rule_type
        self.parameters = parameters
        self.rules_map = {
            "numeric": self._numeric_comparator,
            "percentage": self._percentage_comparator,
            "delta": self._delta_comparator,
            "date": self._date_comparator,
        }

    def _numeric_comparator(self, data) -> bool:
        """
        A comparator class to perform operations on numeric data.

        :param data: A Pandas Series with the company information.
        :return: A boolean to represent the application of the rule.
        """
        desired_operator = self.parameters["operator"]
        desired_field = data.get(self.parameters["field"])

        if desired_operator == "range":
            desired_min = self.parameters["min"]
            desired_max = self.parameters["max"]
            return desired_min <= desired_field <= desired_max

        target_value = self.parameters["value"]
        try:
            return apply_operation(
                desired_field, desired_operator, target_value
            )
        except Exception:
            raise InvalidOperationException(
                message=(
                    "There was an error while performing the operation. "
                    "Please check your rules.yaml and project documentation."
                )
            )

    def _percentage_comparator(self, data) -> bool:
        """
        A comparator class to perform operations on percentages.

        :param data: A Pandas Series with the company information.
        :return: A boolean to represent the application of the rule.
        """
        operator = self.parameters["operator"]
        field = data.get(self.parameters["field"])

        # Locating the number to compare with the 100% reference
        if self.parameters["locator"]:
            company_number = json.loads(field)[self.parameters["locator"]]
        else:
            company_number = field

        # If it's a range calculation, compare with boundaries
        if operator == "range":
            op_min = self.parameters["min"]
            op_max = self.parameters["max"]
            return op_min <= field <= op_max
        try:
            # Getting the total and then calculating the int for the desired %
            total = self.parameters["reference"]
            if total is int:
                final_percent = floor((100 * company_number) / total)
                target_percent = self.parameters["value"]
                return apply_operation(final_percent, operator, target_percent)
            else:
                total = data.get(self.parameters["reference"])
                final_percent = (100 * company_number) / total
                target_percent = self.parameters["value"]
                return apply_operation(final_percent, operator, target_percent)
        except Exception:
            raise InvalidOperationException(
                message=(
                    "There was an error while performing the operation. "
                    "Please check your rules.yaml and project documentation."
                )
            )

    def _delta_comparator(self, data) -> bool:
        """
        A comparator class to perform operations on deltas.

        :param data: A Pandas Series with the company information.
        :return: A boolean to represent the application of the rule.
        """
        operator = self.parameters["operator"]
        flattened_series = []
        series_length = len(self.parameters["series"])
        for i in range(series_length):
            value = data.get(self.parameters["series"][i]["field"], 0)
            if value == 0:
                continue

            # Getting the factor to flatten the series based on the ref_unit
            unit_span = self.parameters["series"][i]["unit_span"]
            mutiplying_factor = self.parameters["ref_unit"] / unit_span

            flattened_series.append(value * mutiplying_factor)

        if len(flattened_series) == 0:
            return False

        series_array = np.array(flattened_series)
        diff = np.diff(series_array)
        variations = []
        for index, num in enumerate(diff):
            if num < 0:
                num *= -1
            other_num = flattened_series[index]
            variations.append(np.round(num / other_num, 2))

        # If it's a range calculation, compare with boundaries
        if operator == "range":
            op_min = self.parameters["min"]
            op_max = self.parameters["max"]
            for number in variations:
                return op_min <= number <= op_max
        else:
            try:
                value = self.parameters["value"]
                return all(
                    [
                        apply_operation(number, operator, value)
                        for number in variations
                    ]
                )

            except Exception:
                raise InvalidOperationException(
                    message=(
                        "There was an error while performing the operation. "
                        "Please check your rules.yaml and project documentation."
                    )
                )

    def _date_comparator(self, data) -> bool:
        """
        A comparator class to perform operations on dates.

        :param data: A Pandas Series with the company information.
        :return: A boolean to represent the application of the rule.
        """
        operator = self.parameters["operator"]
        field_value = data.get(self.parameters["field"], None)
        # If the date of the company, return False
        if field_value is None:
            return False

        if operator == "range":
            desired_min = self.parameters["min"]
            desired_max = self.parameters["max"]
            return desired_min <= field_value <= desired_max

        if self.parameters.get("year", None):
            target_year = self.parameters["year"]
            return apply_operation(target_year, operator, field_value)

        target_value = self.parameters["value"]
        date_options = {
            "current_year": datetime.now().year,
            "last_year": datetime.now().year - 1,
        }
        reference_param_date = self.parameters["reference_date"]

        date_ref = date_options.get(reference_param_date, reference_param_date)
        delta = date_ref - field_value
        try:
            return apply_operation(delta, operator, target_value)
        except Exception:
            raise InvalidOperationException(
                message=(
                    "There was an error while performing the operation. "
                    "Please check your rules.yaml and project documentation."
                )
            )

    def apply_rule(self, data) -> bool:
        return self.rules_map[self.rule_type](data)


class DynamicRulesEngine:
    """This class implements dynamic business rules.
    It extracts its set of rules from the `rules.yaml` file.
    """

    def __init__(self) -> None:
        self.rules_manager = InvestorRulesManager()
        if not self.rules_manager.rules:
            raise InsufficientRulesException()

    @staticmethod
    def _parse_rule(rule_data: dict) -> List[Rule] | Rule:
        """
        Individual Rule parser.
        :param rule_data: A dict from a yaml rule file.
        :return: A Rule object.
        """
        new_rule = Rule(
            rule_id=rule_data["id"],
            name=rule_data["name"],
            rule_type=rule_data["parameters"]["type"],
            parameters=rule_data["parameters"],
        )
        return new_rule

    def parse_rules(self) -> List[Rule]:
        """
        Individual Rule parser.
        :return: A list of Rule objects.
        """
        all_rules_ids = self.rules_manager.get_all_rules()
        if len(all_rules_ids) > 1:
            return [
                self._parse_rule(rule)
                for rule in self.rules_manager.rules.values()
            ]
        else:
            return self._parse_rule(
                self.rules_manager.rules[all_rules_ids.first()]
            )


class StaticRulesEngine:
    """
    This class implements basic/static business rules.
    """

    @staticmethod
    def has_20_to_60_employees(total_employees: int) -> bool:
        """
        Check if the number of employees is within the range

        :param total_employees: Total number of employees.
        :return: A boolean to represent the application of the rule.
        """
        return 20 <= total_employees <= 60

    @staticmethod
    def most_of_employees_are_us_based(employee_locations: dict) -> bool:
        """
        Check if the number of employees that are US-based is enough.

        :param employee_locations: Dictionary of employee locations
        :return: A boolean to represent the application of the rule.
        """
        list_of_employees = [value for value in employee_locations.values()]
        us_based_employees = employee_locations.get("USA", 0)
        if us_based_employees == 0:
            return False
        else:
            employees_total = sum(list_of_employees)
            required_employees_in_us = employees_total * 0.7
            return us_based_employees >= floor(required_employees_in_us)

    @staticmethod
    def is_us_based(headquarters):
        """
        Check if the company's headquarters is the USA

        :param headquarters: The country code.
        :return: A boolean to represent the application of the rule.
        """
        """"""
        term = r"(usa|united states)"
        match = re.search(term, headquarters.lower(), re.IGNORECASE)
        if match:
            return True
        else:
            return False

    @staticmethod
    def is_founded_in_last_5_years(founding_year: int) -> bool:
        """
        Check if company was founded in last 5 years

        :param founding_year: The year that the company was founded
        :return: A boolean to represent the application of the rule.
        """
        if founding_year is None or founding_year <= 0:
            return False
        else:
            today = datetime.now().year
            delta = today - founding_year
            return True if delta <= 5 else False

    @staticmethod
    def is_saas_company(business_description: str) -> bool:
        """
        Determine if company is a SaaS company
        - Using regex to match specific patterns
        - Looking for keywords
        - Analyzing the business model through keywords

        :param business_description: A string describing the business.
        :return: A boolean to represent the application of the rule.
        """
        rejection_patterns = [
            "hardware",
            r"(hardware|equipment).{0,30}(purchase|sold)",
            r"(one-time|single).{0,30}(purchase)",
        ]

        saas_search_patterns = [
            "cloud-based",
            "software solution",
            "platform as a service",
            "subscription-based",
            "subscription based",
            "subscription model",
            "annual subscription model",
            "scalable solution",
            r"(streamline).{0,30}(workflow|operation|operations)",
            r"(scalable|scale).{0,30}(solution|software|operation|operations)",
            r"(monthly|annual).{0,30}(subscription|software|operation|operations|fee|fees|pricing|billing)",
            r"(recurring|platform).{0,30}(subscription|subscriptions|fees|cost|billing)",
            r"(agent-based|user-based|usage-based|node-based).{0,30}(pricing)",
        ]
        for term in rejection_patterns:
            text = business_description.lower()
            try:
                match = re.search(term, text, re.IGNORECASE)
                if match:
                    return False
            except re.error:
                if term in text:
                    return False

        for term in saas_search_patterns:
            text = business_description.lower()
            try:
                match = re.search(term, text, re.IGNORECASE)
                if match:
                    return True
            except re.error:
                if term in text:
                    return True
        return False
