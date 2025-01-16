import logging
import os
import subprocess
from pathlib import Path
from typing import Callable, Generator

import pytest
from pyspark.sql import SparkSession

from testsession_configuration import TestSessionConfiguration


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


import yaml

from container_tests.databricks_api_client import DatabricksApiClient
from test_configuration import TestConfiguration


@pytest.fixture(autouse=True)
def configure_dummy_logging() -> None:
    """Ensure that logging hooks don't fail due to _TRACER_NAME not being set."""

    from telemetry_logging.logging_configuration import configure_logging

    configure_logging(
        cloud_role_name="any-cloud-role-name", tracer_name="any-tracer-name"
    )


@pytest.fixture(scope="session")
def file_path_finder() -> Callable[[str], str]:
    """
    Returns the path of the file.
    Please note that this only works if current folder haven't been changed prior using
    `os.chdir()`. The correctness also relies on the prerequisite that this function is
    actually located in a file located directly in the tests folder.
    """

    def finder(file: str) -> str:
        return os.path.dirname(os.path.normpath(file))

    return finder


@pytest.fixture(scope="session")
def source_path(file_path_finder: Callable[[str], str]) -> str:
    """
    Returns the <repo-root>/source folder path.
    Please note that this only works if current folder haven't been changed prior using
    `os.chdir()`. The correctness also relies on the prerequisite that this function is
    actually located in a file located directly in the tests folder.
    """
    return file_path_finder(f"{__file__}/../..")


@pytest.fixture(scope="session")
def capacity_settlement_tests_path(source_path: str) -> str:
    """
    Returns the tests folder path for capacity settlement.
    """
    return f"{source_path}/capacity_settlement/tests"


@pytest.fixture(scope="session")
def tests_path(file_path_finder: Callable[[str], str]) -> str:
    """Returns the tests folder path."""
    return file_path_finder(f"{__file__}")


@pytest.fixture(scope="session")
def capacity_settlement_path(source_path: str) -> str:
    """
    Returns the source/capacity_settlement/ folder path.
    Please note that this only works if current folder haven't been changed prior using
    `os.chdir()`. The correctness also relies on the prerequisite that this function is
    actually located in a file located directly in the tests folder.
    """
    return f"{source_path}/capacity_settlement/src"


@pytest.fixture(scope="session")
def contracts_path(capacity_settlement_path: str) -> str:
    """
    Returns the source/contract folder path.
    Please note that this only works if current folder haven't been changed prior using
    `os.chdir()`. The correctness also relies on the prerequisite that this function is
    actually located in a file located directly in the tests folder.
    """
    return f"{capacity_settlement_path}/contracts"


@pytest.fixture(scope="session")
def virtual_environment() -> Generator:
    """Fixture ensuring execution in a virtual environment.
    Uses `virtualenv` instead of conda environments due to problems
    activating the virtual environment from pytest."""

    # Create and activate the virtual environment
    subprocess.call(["virtualenv", ".test-pytest"])
    subprocess.call(
        "source .test-pytest/bin/activate", shell=True, executable="/bin/bash"
    )

    yield None

    # Deactivate virtual environment upon test suite tear down
    subprocess.call("deactivate", shell=True, executable="/bin/bash")


@pytest.fixture(scope="session")
def installed_package(
    virtual_environment: Generator, capacity_settlement_path: str
) -> None:
    # Build the package wheel
    os.chdir(capacity_settlement_path)
    subprocess.call("python -m build --wheel", shell=True, executable="/bin/bash")

    # Uninstall the package in case it was left by a cancelled test suite
    subprocess.call(
        "pip uninstall -y package",
        shell=True,
        executable="/bin/bash",
    )

    # Install wheel, which will also create console scripts for invoking the entry points of the package
    subprocess.call(
        f"pip install {capacity_settlement_path}/dist/opengeh_capacity_settlement-1.0-py3-none-any.whl",
        shell=True,
        executable="/bin/bash",
    )


def _load_settings_from_file(file_path: Path) -> dict:
    if file_path.exists():
        with file_path.open() as stream:
            return yaml.safe_load(stream)
    else:
        return {}


@pytest.fixture(scope="session")
def test_configuration(
    capacity_settlement_tests_path: str,
) -> TestConfiguration:
    """
    Load settings for tests either from a local YAML settings file or from environment variables.
    Proceeds even if certain Azure-related keys are not present in the settings file.
    """

    settings_file_path = (
        Path(capacity_settlement_tests_path) / "test.local.settings.yml"
    )

    def load_settings_from_env() -> dict:
        return {
            key: os.getenv(key)
            for key in [
                "AZURE_KEYVAULT_URL",
                "AZURE_TENANT_ID",
                "DATABRICKS_HOST",
                "DATABRICKS_TOKEN",
            ]
            if os.getenv(key) is not None
        }

    settings = _load_settings_from_file(settings_file_path) or load_settings_from_env()

    # Set environment variables from loaded settings
    for key, value in settings.items():
        if value is not None:
            os.environ[key] = value

    if "AZURE_KEYVAULT_URL" in settings:
        return TestConfiguration(azure_keyvault_url=settings["AZURE_KEYVAULT_URL"])

    logging.error(
        f"Test configuration could not be loaded from {settings_file_path} or environment variables."
    )
    raise Exception(
        "Failed to load test settings. Ensure that the Azure Key Vault URL is provided in the settings file or as an environment variable."
    )


@pytest.fixture(scope="session")
def databricks_client(test_configuration: TestConfiguration) -> DatabricksApiClient:
    return DatabricksApiClient(
        os.environ["DATABRICKS_HOST"],
        os.environ["DATABRICKS_TOKEN"],
    )


@pytest.fixture(scope="session")
def test_session_configuration(tests_path: str) -> TestSessionConfiguration:
    settings_file_path = Path(tests_path) / "testsession.local.settings.yml"
    return TestSessionConfiguration.load(settings_file_path)
