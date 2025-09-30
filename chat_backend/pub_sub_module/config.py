"""Setting of the analytics_engine

Raises:
    EnvironmentVariableNotSet: _description_
"""

import logging
import os

from dotenv import load_dotenv

from pub_sub_module.logger import logger_config

logging_dict = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}

load_dotenv(verbose=True)


class EnvironmentVariableNotSet(Exception):
    """Error class for loading and managing environment variables"""


class ENV:
    """Environment variables"""

    def __init__(self) -> None:
        """Add environment variables here"""
        self.LOGGING_LEVEL = logging_dict[os.getenv("LOGGING_LEVEL")]
        self.logger = logger_config(self.LOGGING_LEVEL)

        self.BROKER_URL = os.getenv("BROKER_URL")
        self.DATABRICKS_CATALOG_NAME = os.getenv("DATABRICKS_CATALOG_NAME")
        self.DATABRICKS_SERVER_HOST = os.getenv("DATABRICKS_SERVER_HOST")
        self.DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
        self.DATABRICKS_ACCESS_TOKEN = os.getenv("DATABRICKS_ACCESS_TOKEN")

        self.IS_PROD = os.getenv("IS_PROD")

    def check_environment_variable(self):
        """Check if all environment variables are defined

        Raises:
            EnvironmentVariableNotSet: Raise error incase
                any environment variable is not defined
        """
        for _property in dir(self):
            if (
                (getattr(self, _property) is None)
                and (not _property.startswith("__"))
                and (_property.isupper())
            ):
                self.logger.error("LOADING ENVIRONMENT VARIABLE: FAILED!")
                raise EnvironmentVariableNotSet(
                    f"SET {_property} AS AN ENVIRONMENT VARIABLE!"
                )
        self.logger.info("LOADING ENVIRONMENT VARIABLE: SUCEEDED!")


env = ENV()
env.check_environment_variable()
