from typing import Generator

import pytest
import TestSessionConfiguration
import yaml
from pyspark.sql import SparkSession
from telemetry_logging.logging_configuration import configure_logging
from testcommon.container_test import DatabricksApiClient

from tests import PROJECT_ROOT, Path


@pytest.fixture(scope="module", autouse=True)
def clear_cache(spark: SparkSession) -> Generator[None, None, None]:
    yield
    # Clear the cache after each test module to avoid memory issues
    spark.catalog.clearCache()


@pytest.fixture(scope="session")
def spark() -> Generator[SparkSession, None, None]:
    session = SparkSession.builder.appName("testcommon").getOrCreate()
    yield session
    session.stop()


@pytest.fixture(autouse=True)
def configure_dummy_logging() -> None:
    """Ensure that logging hooks don't fail due to _TRACER_NAME not being set."""
    configure_logging(cloud_role_name="any-cloud-role-name", tracer_name="any-tracer-name")


@pytest.fixture(scope="session")
def contracts_path() -> str:
    """
    Returns the source/contract folder path.
    Please note that this only works if current folder haven't been changed prior using
    `os.chdir()`. The correctness also relies on the prerequisite that this function is
    actually located in a file located directly in the tests folder.
    """
    return f"{PROJECT_ROOT}/contracts"


@pytest.fixture(scope="session")
def test_session_configuration() -> TestSessionConfiguration:  # noqa: F821
    settings_file_path = PROJECT_ROOT / "tests" / "testsession.local.settings.yml"
    return TestSessionConfiguration.load(settings_file_path)


def _load_settings_from_file(file_path: Path) -> dict:
    if file_path.exists():
        with file_path.open() as stream:
            return yaml.safe_load(stream)
    else:
        return {}


@pytest.fixture(scope="session")
def databricks_api_client() -> DatabricksApiClient:
    settings = _load_settings_from_file(PROJECT_ROOT / "tests" / "test.local.settings.yml")
    databricks_token = settings.get("DATABRICKS_TOKEN")
    databricks_host = settings.get("WORKSPACE_URL")
    databricksApiClient = DatabricksApiClient(databricks_token, databricks_host)
    return databricksApiClient
