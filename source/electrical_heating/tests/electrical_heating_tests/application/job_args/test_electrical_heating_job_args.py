import uuid
from unittest.mock import patch

import pytest

from opengeh_electrical_heating.application.job_args.electrical_heating_args import (
    ElectricalHeatingArgs,
)
from opengeh_electrical_heating.application.job_args.environment_variables import (
    EnvironmentVariable,
)

DEFAULT_ORCHESTRATION_INSTANCE_ID = uuid.UUID("12345678-9fc8-409a-a169-fbd49479d711")
DEFAULT_TIME_ZONE = "Europe/Copenhagen"
DEFAULT_CATALOG_NAME = "some_catalog"
ELECTRICITY_MARKET_DATA_PATH = "some_market_path"


def _get_contract_parameters(filename: str) -> list[str]:
    with open(filename) as file:
        text = file.read()
        text = text.replace("{orchestration-instance-id}", str(DEFAULT_ORCHESTRATION_INSTANCE_ID))
        lines = text.splitlines()
        return list(filter(lambda line: not line.startswith("#") and len(line) > 0, lines))


@pytest.fixture(scope="session")
def contract_parameters(contracts_path: str) -> list[str]:
    job_parameters = _get_contract_parameters(f"{contracts_path}/parameters-reference.txt")
    return job_parameters


@pytest.fixture(scope="session")
def sys_argv_from_contract(
    contract_parameters: list[str],
) -> list[str]:
    return ["dummy_script_name"] + contract_parameters


@pytest.fixture(scope="session")
def job_environment_variables() -> dict:
    return {
        EnvironmentVariable.CATALOG_NAME.name: "some_catalog",
        EnvironmentVariable.TIME_ZONE.name: "Europe/Copenhagen",
        EnvironmentVariable.ORCHESTRATION_INSTANCE_ID.name: str(DEFAULT_ORCHESTRATION_INSTANCE_ID),
        EnvironmentVariable.ELECTRICITY_MARKET_DATA_PATH.name: str(ELECTRICITY_MARKET_DATA_PATH),
    }


def test_when_parameters__parses_parameters_from_contract(
    job_environment_variables: dict,
    sys_argv_from_contract: list[str],
) -> None:
    """
    This test ensures that the job accepts
    the arguments that are provided by the client.
    """
    # Arrange
    with patch("sys.argv", sys_argv_from_contract):
        with patch.dict("os.environ", job_environment_variables):
            actual_args = ElectricalHeatingArgs()

    # Assert
    assert actual_args.orchestration_instance_id == DEFAULT_ORCHESTRATION_INSTANCE_ID
    assert actual_args.time_zone == DEFAULT_TIME_ZONE
    assert actual_args.catalog_name == DEFAULT_CATALOG_NAME
