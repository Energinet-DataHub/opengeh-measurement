import os
from enum import Enum
from typing import Any


# TODO: Move to shared library
class EnvironmentVariable(Enum):
    CATALOG_NAME = "CATALOG_NAME"
    TIME_ZONE = "TIME_ZONE"
    ORCHESTRATION_INSTANCE_ID = "ORCEHSTRATION_INSTANCE_ID"
    ELECTRICITY_MARKET_DATA_PATH = "ELECTRICITY_MARKET_DATA_PATH"


def get_catalog_name() -> str:
    return get_env_variable_or_throw(EnvironmentVariable.CATALOG_NAME)


def get_time_zone() -> str:
    return get_env_variable_or_throw(EnvironmentVariable.TIME_ZONE)


def get_orchestration_instance_id() -> str:
    return get_env_variable_or_throw(EnvironmentVariable.ORCHESTRATION_INSTANCE_ID)


def get_electricity_market_data_path() -> str:
    return get_env_variable_or_throw(EnvironmentVariable.ELECTRICITY_MARKET_DATA_PATH)


def get_env_variable_or_throw(variable: EnvironmentVariable) -> Any:
    env_variable = os.getenv(variable.name)
    if env_variable is None:
        raise ValueError(f"Environment variable not found: {variable.name}")

    return env_variable
