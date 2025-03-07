import os
from pathlib import Path

import yaml

from src.exceptions import InsufficientRulesException


class InvestorRulesManager:
    def __init__(self, rules_file_path="rules.yml"):
        self.rules_file_path = Path(rules_file_path)
        self.rules = {}
        self._load_rules()

    def _load_rules(self):
        """
        Load all investor rules from YAML file

        :return: None
        """

        env_config_path = os.environ.get("RULES_CONFIG_FILE")

        rules_paths = [
            env_config_path,
            Path(__file__).cwd() / "rules.yml",
            Path(__file__).cwd() / "rules.yaml",
            ]

        for path in rules_paths:
            if path and Path(path).exists():
                try:
                    with open(path, "r") as file:
                        data = yaml.safe_load(file)

                    # Process each rule
                    for rule in data.get("rules", []):
                        rule_id = rule.get("id")
                        if rule_id:
                            self.rules[rule_id] = rule
                    return
                except (IOError, yaml.YAMLError) as e:
                    print(f"Error loading rules from {path}: {e}")

        raise InsufficientRulesException()

    def get_all_rules(self):
        """Return all rules' IDs"""
        return list(self.rules.keys())

    def rule_exists(self, rule_id):
        """Check if a rule exists"""
        return rule_id in self.rules
