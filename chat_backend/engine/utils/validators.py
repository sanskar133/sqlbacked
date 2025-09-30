"""Utility functions for variable validation"""

from settings import env
from utils import commons


@commons.error_decorator(error_type=ValueError)
def validate_database_type(database_type: str):
    """Check if database_type is supported by the system

    Args:
        database_type (str): user's database type

    Raises:
        ValueError: Raise value error if database_type is not supported
    """
    if database_type not in env.SUPPORTED_DATABASE_TYPES:
        raise ValueError(
            "SQLGenerator: database_type must be one of %r."
            % env.SUPPORTED_DATABASE_TYPES
        )
