"""Setting of the analytics_engine

Raises:
    EnvironmentVariableNotSet: _description_
"""

import logging
import os

from dotenv import load_dotenv
from utils.secure_env import decrypt_envvar

logging_dict = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}

env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
print(env_file_path, os.path.exists(env_file_path))
load_dotenv(dotenv_path=env_file_path, verbose=True, override=True)
print(os.getenv("LLM_PROVIDER"))


class EnvironmentVariableNotSet(Exception):
    """Error class for loading and managing environment variables"""


class ENV:
    """Environment variables"""

    def __init__(self) -> None:
        """Add environment variables here"""
        self.LOGGING_LEVEL = logging_dict.get(os.getenv("LOGGING_LEVEL"), "info")
        # self.logger = logger_config(self.LOGGING_LEVEL)

        # self.DATABRICKS_SERVER_HOST = os.getenv("DATABRICKS_SERVER_HOST")
        # self.DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
        # self.DATABRICKS_ACCESS_TOKEN = os.getenv("DATABRICKS_ACCESS_TOKEN")
        # self.ECOM_INDEX_NAME = os.getenv("ECOM_INDEX_NAME")
        # self.DATABRICKS_TABLE_PREFIX = os.getenv("DATABRICKS_TABLE_PREFIX")

        # Get connection metadata
        self.CONNECTION_META_DATA = {}
        
        if os.getenv("ACCESS_ID_PRESALES_DEMO_ECOM"):
            self.CONNECTION_META_DATA.update(
                {
                    os.getenv("ACCESS_ID_PRESALES_DEMO_ECOM"): {
                        "database_type": os.getenv("DB_TYPE_PRESALES_DEMO_ECOM"),
                        "database_meta_data": {
                            "database": os.getenv("DB_LINK_PRESALES_DEMO_ECOM"),
                        },
                    }
                }
            )
        
        if os.getenv("ACCESS_ID_PRESALES_DEMO_LOAN"):
            self.CONNECTION_META_DATA.update(
                {
                    os.getenv("ACCESS_ID_PRESALES_DEMO_LOAN"): {
                        "database_type": os.getenv("DB_TYPE_PRESALES_DEMO_LOAN"),
                        "database_meta_data": {
                            "database": os.getenv("DB_LINK_PRESALES_DEMO_LOAN"),
                        },
                    }
                }
            )
        
        if os.getenv("ACCESS_ID_DATABRICKS_SQL"):
            self.CONNECTION_META_DATA.update(
                {
                    os.getenv("ACCESS_ID_DATABRICKS_SQL"): {
                        "database_type": os.getenv("DB_TYPE_DATABRICKS_SQL"),
                        "database_meta_data": {
                            "server_hostname": os.getenv("DB_HOST_DATABRICKS_SQL"),
                            "http_path": os.getenv("DB_HTTP_PATH_DATABRICKS_SQL"),
                            "access_token": decrypt_envvar(
                                os.getenv("DB_ACCESS_TOKEN_DATABRICKS_SQL")
                            ),
                        },
                    }
                }
            )
        # Analytics Engine ENV Variables

        self.SUPPORTED_DATABASE_TYPES = [
            "Postgres",
            "Snowflake",
            "Databricks",
            "Mssql",
            "Ibm_i_db2",
            "Sqlite3",
        ]

        self.LLM_PROVIDER = os.getenv("LLM_PROVIDER")
        self.LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
        self.LLM_API_KEY = os.getenv("LLM_API_KEY")
        if self.LLM_PROVIDER == "AZURE":
            self.LLM_API_ENDPOINT = os.getenv("LLM_API_ENDPOINT")
            self.LLM_API_TYPE = os.getenv("LLM_API_TYPE")
            self.LLM_API_VERSION = os.getenv("LLM_API_VERSION")

        # self.OPENAI_LLM_API_KEY = os.getenv("OPENAI_LLM_API_KEY")
        # self.OPENAI_LLM_MODEL_NAME = os.getenv("OPENAI_LLM_MODEL_NAME")

        # VectorDB ENV Variables
        # self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
        # self.ELASTIC_SEARCH_URL = os.getenv("ELASTIC_SEARCH_URL")
        # self.EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION"))

        # RCA ENV Variables
        self.MODE = os.getenv("MODE", "dev")
        # Fabric Auth Variables:
        self.FABRIC_SERVER = decrypt_envvar(os.getenv("FABRIC_SERVER"))
        self.FABRIC_SERVER_TOKEN = decrypt_envvar(os.getenv("FABRIC_SERVER_TOKEN"))
        self.FABRIC_CLIENT = decrypt_envvar(os.getenv("FABRIC_CLIENT"))
        self.FABRIC_TOKEN = decrypt_envvar(os.getenv("FABRIC_TOKEN"))

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
                print("LOADING ENVIRONMENT VARIABLE: FAILED!")
                raise EnvironmentVariableNotSet(
                    f"SET {_property} AS AN ENVIRONMENT VARIABLE!"
                )
        print("LOADING ENVIRONMENT VARIABLE: SUCEEDED!")


env = ENV()

env.check_environment_variable()
