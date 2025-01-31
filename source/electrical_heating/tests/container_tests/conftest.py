import pytest
from container_tests.environment_configuration import EnvironmentConfiguration
from testcommon.container_test import DatabricksApiClient


@pytest.fixture(scope="session")
def environment_configuration() -> EnvironmentConfiguration:
    return EnvironmentConfiguration()


@pytest.fixture(scope="session")
def databricks_api_client(environment_configuration: EnvironmentConfiguration) -> DatabricksApiClient:
    databricksApiClient = DatabricksApiClient(
        environment_configuration.databricks_token,
        environment_configuration.databricks_workspace_url,
    )
    return databricksApiClient
