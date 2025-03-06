from unittest.mock import patch

from src.rules_engine import StaticRulesEngine


class TestStaticRulesEngine:
    def test_has_20_to_60_employees(self):
        # Test with exactly 20 employees
        assert (
            StaticRulesEngine.has_20_to_60_employees({"USA": 10, "Canada": 10}) is True
        )

        # Test with exactly 60 employees
        assert (
            StaticRulesEngine.has_20_to_60_employees(
                {"USA": 30, "Canada": 15, "UK": 15}
            ) is True
        )

        # Test with employees within range
        assert (
            StaticRulesEngine.has_20_to_60_employees(
                {"USA": 25, "Canada": 10, "UK": 5}
            ) is True
        )

        # Test with less than 20 employees
        assert (
            StaticRulesEngine.has_20_to_60_employees({"USA": 10, "Canada": 9}) is False
        )

        # Test with more than 60 employees
        assert (
            StaticRulesEngine.has_20_to_60_employees(
                {"USA": 40, "Canada": 30, "UK": 20}
            ) is False
        )

        # Test with empty dictionary
        assert StaticRulesEngine.has_20_to_60_employees({}) is False

    def test_most_of_employees_are_us_based(self):
        # Test with more than 70% US employees
        assert (
            StaticRulesEngine.most_of_employees_are_us_based(
                {"USA": 35, "Canada": 10, "UK": 5}
            ) is True
        )

        # Test with exactly 70% US employees
        assert (
            StaticRulesEngine.most_of_employees_are_us_based(
                {"USA": 35, "Canada": 15}
            ) is True
        )

        # Test with less than 70% US employees
        assert (
            StaticRulesEngine.most_of_employees_are_us_based(
                {"USA": 30, "Canada": 20, "UK": 10}
            ) is False
        )

        # Test with no US employees
        assert (
            StaticRulesEngine.most_of_employees_are_us_based(
                {"Canada": 30, "UK": 20}
            ) is False
        )

        # Test with edge case - single employee in US
        assert (
            StaticRulesEngine.most_of_employees_are_us_based({"USA": 1}) is True
        )

        # Test with exactly floor(70%) employees in US
        assert (
            StaticRulesEngine.most_of_employees_are_us_based(
                {"USA": 7, "Canada": 3}
            ) is True
        )

    def test_is_us_based(self):
        # Test with "USA"
        assert StaticRulesEngine.is_us_based("USA") is True

        # Test with "United States"
        assert StaticRulesEngine.is_us_based("United States") is True

        # Test with a mixed case
        assert StaticRulesEngine.is_us_based("united STATES") is True

        # Test with string containing the word USA
        assert StaticRulesEngine.is_us_based("Headquarters in USA") is True

        # Test with string containing the word United States
        assert (
            StaticRulesEngine.is_us_based(
                "Based in the United States of America"
            ) is True
        )

        # Test with non-US country
        assert StaticRulesEngine.is_us_based("Canada") is False

        # Test with empty string
        assert StaticRulesEngine.is_us_based("") is False

    @patch("datetime.datetime")
    def test_is_founded_in_last_5_years(self, mock_datetime):
        # Set the current year to 2025 for tests
        mock_datetime.now.return_value.year = 2025

        # Test with company founded exactly 5 years ago
        assert StaticRulesEngine.is_founded_in_last_5_years(2020) is True

        # Test with company founded less than 5 years ago
        assert StaticRulesEngine.is_founded_in_last_5_years(2022) is True

        # Test with company founded in the current year
        assert StaticRulesEngine.is_founded_in_last_5_years(2025) is True

        # Test with company founded more than 5 years ago
        assert StaticRulesEngine.is_founded_in_last_5_years(2019) is False


    def test_is_saas_company(self):
        # Test with obvious SaaS descriptors
        assert (
            StaticRulesEngine.is_saas_company(
                "A cloud-based platform providing subscription-based services"
            )
            is True
        )
        assert (
            StaticRulesEngine.is_saas_company(
                "Software solution with annual subscription model"
            )
            is True
        )
        assert (
            StaticRulesEngine.is_saas_company("Platform as a service offering")
            is True
        )

        # Test with less obvious SaaS indicators
        assert (
            StaticRulesEngine.is_saas_company(
                "Our software helps streamline workflow operations"
            )
            is True
        )
        assert (
            StaticRulesEngine.is_saas_company(
                "We offer scalable solutions with monthly subscription fees"
            ) is True
        )
        assert (
            StaticRulesEngine.is_saas_company(
                "User-based pricing structure for our enterprise software"
            ) is True
        )

        # Test with rejection patterns
        assert (
            StaticRulesEngine.is_saas_company(
                "We sell hardware equipment purchased by businesses"
            ) is False
        )
        assert (
            StaticRulesEngine.is_saas_company(
                "One-time purchase of our product"
            ) is False
        )
        assert (
            StaticRulesEngine.is_saas_company(
                "Software with single purchase licensing model"
            ) is False
        )

        # Test with mixed indicators
        assert (
            StaticRulesEngine.is_saas_company(
                "Monthly subscription service but hardware is sold separately"
            ) is False
        )

        # Test with non-matching string
        assert (
            StaticRulesEngine.is_saas_company(
                "We provide consultancy services"
            ) is False
        )

        # Test with empty string
        assert StaticRulesEngine.is_saas_company("") is False
