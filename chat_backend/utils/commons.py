"""Commnon utility functions which can be use across the module."""

import logging
import traceback

import requests
from settings import env

logger = logging.getLogger(__name__)


def error_decorator(error_type: Exception, raise_exc: bool = True):
    """Decorator to enable error logging and raise exceptions

    Args:
        error_type (Exception): Type of error for which to log the errors
        raise_exc (bool): raise error and stop the function if True
            else only logs the error
    """

    def error_func(func):
        def func_wrapper(*args, **kwargs):
            try:
                returned_value = func(*args, **kwargs)
                return returned_value
            except error_type as exc:
                logger.error(exc)
                if raise_exc:
                    raise exc
                return None

        return func_wrapper

    return error_func


def authenticate():
    # response = requests.post(
    #     url=f"{env.FABRIC_SERVER}/authenticate",
    #     headers={"Authorization": f"Basic {env.FABRIC_SERVER_TOKEN}"},
    #     json={"client_id": env.FABRIC_CLIENT, "token": env.FABRIC_TOKEN},
    # )
    # try:
    #     response = response.json()
    #     if response["authenticate"]:
    #         return True, ""
    #     else:
    #         return False, response["message"]
    # except:
    #     return False, traceback.format_exc()
    return True, "Authenticated"
