"""
Parses user defined processing logic.
"""

import re
from datetime import datetime
from math import floor
from typing import List
from xmlrpc.client import DateTime

from src.exceptions import InsufficientRulesException


class Rule:
    def __init__(
        self,
        name: str,
        rule_id: str,
        comparator: str,
        rule_type: str,
    ):
        self.rule_id = rule_id
        self.name = name
        self.rule_type = rule_type
        self.comparator = comparator

    def _numeric_within_range(self):
        pass

    def _numeric_exact_match(self, a: int, b: int) -> bool:
        return a == b

    def _numeric_greater_than(self):
        pass

    def _numeric_lesser_than(self):
        pass

    def _date_within_range(self):
        pass

    def _date_exact_match(self, a: DateTime, b: DateTime):
        return a == b

    def _date_greater_than(self):
        pass

    def _date_lesser_than(self):
        pass

    def apply_rule(self, data):
        rules_map = {
            "numeric": {
                "within_range": self._numeric_within_range,
                "exact_match": self._numeric_exact_match,
                "greater_than": self._numeric_greater_than,
                "lesser_than": self._numeric_lesser_than,
            },
            "date": {
                "within_range": self._date_within_range,
                "exact_match": self._date_exact_match,
                "greater_than": self._date_greater_than,
                "lesser_than": self._date_lesser_than,
            },
        }
        return rules_map[self.rule_type][self.comparator](data)


class RuleProcessor:
    def __init__(self, rules_set: list) -> None:
        if not rules_set:
            raise InsufficientRulesException()
        self.rules_set = rules_set

    @staticmethod
    def _parse_rule(self, **kwargs) -> Rule:
        rule_type = kwargs.pop("type")
        new_rule = Rule(**kwargs, rule_type=rule_type)
        return new_rule

    @staticmethod
    def parse_rules(self, rules_list) -> List[Rule]:
        if len(self.rules_set) > 1:
            return [self.parse_rule(rule) for rule in rules_list]
        else:
            return self.parse_rule(rules_list[0])


class StaticRulesEngine:
    """This class implements basic/static business rules.
    Will be replaced by dynamic setting of rules, via JSON.
    """

    @staticmethod
    def has_20_to_60_employees(employee_locations: dict) -> bool:
        """Check if the number of employees is within the range"""
        list_of_employees = [value for value in employee_locations.values()]
        return 20 <= sum(list_of_employees) <= 60

    @staticmethod
    def most_of_employees_are_us_based(employee_locations: dict) -> bool:
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
        """Check if the company's headquarters is US"""
        term = r"(usa|united states)"
        match = re.search(term, headquarters.lower(), re.IGNORECASE)
        if match:
            return True
        else:
            return False

    @staticmethod
    def is_founded_in_last_5_years(founding_year: int) -> bool:
        """Check if company was founded in last 5 years"""
        today = datetime.now().year
        delta = today - founding_year
        return True if delta <= 5 else False

    @staticmethod
    def is_saas_company(business_description: str) -> bool:
        """Determine if company is a SaaS company
        - Using regex to match specific patterns
        - Looking for keywords
        - Analyzing the business model through keywords
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
