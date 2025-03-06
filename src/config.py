"""
Project's configuration parser for the Investment Company Classifier.
"""

import logging
import os
from pathlib import Path

import yaml

from src.exceptions import ImproperlyConfiguredException


class ConfigManager:
    _instance = None
    _config = None
    _logger = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the class
        - Load configuration
        - Setup logging
        - Validate critical configuration
        """
        self._load_config()
        self._setup_logging()
        self._validate_config()

    def _load_config(self):
        """Load configuration from sources
        Priority:
            1. Environment variable
            2. Default config file
            3. Raise exception
        """

        env_config_path = os.environ.get("CLASSIFIER_CONFIG_FILE")

        config_paths = [
            env_config_path,
            Path(__file__).cwd() / "config.yml",
            Path(__file__).cwd() / "config.yaml",
        ]

        for path in config_paths:
            if path and Path(path).exists():
                try:
                    with open(path, "r") as file:
                        self._config = yaml.safe_load(file)
                    return
                except (IOError, yaml.YAMLError) as e:
                    print(f"Error loading config from {path}: {e}")

        raise ImproperlyConfiguredException(
            message="No valid configuration file found",
            parameter_name="CLASSIFIER_CONFIG_FILE",
        )

    def _setup_logging(self):
        """
        Configure logging based on config settings
        """
        log_config = self._config.get("logging", {})
        log_level = getattr(logging, log_config.get("level", "INFO").upper())
        log_file = log_config.get("file_path", "app.log")

        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Configure logging
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )
        self._logger = logging.getLogger(__name__)

    def _validate_config(self):
        """
        Perform critical configuration validation
        Check for required configuration sections and values
        """
        required_sections = [
            "data_sources.input_base_path",
            "data_sources.output_base_path",
            "data_sources.input_filename",
            "investor_rules",
        ]

        for section in required_sections:
            if not self.get(section):
                self._logger.error(
                    f"Missing critical configuration: {section}"
                )
                raise ImproperlyConfiguredException(
                    message="Missing critical configuration.",
                    parameter_name=section,
                )

    def get(self, key, default=None):
        """
        Retrieve nested configuration values

        Args:
            key (str): Dot-separated configuration key
            default: Value to return if key is not found

        Returns:
            Configuration value or default
        """
        if not self._config:
            raise ImproperlyConfiguredException(
                "Configuration not loaded", parameter_name=key
            )

        keys = key.split(".")
        value = self._config

        try:
            for k in keys:
                value = value.get(k, {})
                if value == {}:
                    return default
            return value if value != {} else default
        except Exception as e:
            self._logger.error(f"Error retrieving config key {key}: {e}")
            return default

    def reload(self):
        """
        Reload configuration from file
        Useful for dynamic configuration updates
        """
        self._load_config()
        self._setup_logging()
        self._validate_config()

    def as_dict(self):
        """
        Return full configuration as dict
        """
        return self._config.copy()


config = ConfigManager()
