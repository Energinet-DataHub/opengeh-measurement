### This file contains the fixtures that are used in the tests. ###
from pathlib import Path
from typing import Generator

import pytest
from delta import configure_spark_with_delta_pip
from pyspark.sql import DataFrame, SparkSession
from telemetry_logging.logging_configuration import configure_logging
from testcommon.delta_lake import create_database, create_table

from opengeh_electrical_heating.infrastructure.measurements_bronze.database_definitions import (
    MeasurementsBronzeDatabase,
)
from opengeh_electrical_heating.infrastructure.measurements_bronze.schemas.measurements_bronze_v1 import (
    measurements_bronze_v1,
)
from opengeh_electrical_heating.infrastructure.measurements_gold.database_definitions import (
    MeasurementsGoldDatabase,
)
from opengeh_electrical_heating.infrastructure.measurements_gold.schemas.time_series_points_v1 import (
    time_series_points_v1,
)
from tests import PROJECT_ROOT
from tests.testsession_configuration import TestSessionConfiguration
from tests.utils.delta_table_utils import (
    read_from_csv,
)
from tests.utils.measurements_utils import create_measurements_dataframe


@pytest.fixture(scope="module", autouse=True)
def clear_cache(spark: SparkSession) -> Generator[None, None, None]:
    """
    Clear the cache after each test module to avoid memory issues.
    """
    yield
    spark.catalog.clearCache()


@pytest.fixture(scope="session")
def spark() -> Generator[SparkSession, None, None]:
    """
    Create a Spark session with Delta Lake enabled.
    """
    session = (
        SparkSession.builder.appName("testcommon")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        # Enable Hive support for persistence across test sessions
        .config("spark.sql.catalogImplementation", "hive")
        .enableHiveSupport()
    )
    session = configure_spark_with_delta_pip(session).getOrCreate()
    yield session
    session.stop()


@pytest.fixture(autouse=True)
def configure_dummy_logging() -> None:
    """Ensure that logging hooks don't fail due to _TRACER_NAME not being set."""

    configure_logging(cloud_role_name="any-cloud-role-name", tracer_name="any-tracer-name")


@pytest.fixture(scope="session")
def tests_path() -> str:
    """Returns the tests folder path."""
    return (PROJECT_ROOT / "tests").as_posix()


@pytest.fixture(scope="session")
def contracts_path() -> str:
    """Returns the source/contract folder path."""
    return (PROJECT_ROOT / "contracts").as_posix()


@pytest.fixture(scope="session")
def test_files_folder_path(tests_path: str) -> str:
    return f"{tests_path}/utils/test_files"


@pytest.fixture(scope="session")
def test_session_configuration(tests_path: str) -> TestSessionConfiguration:
    settings_file_path = Path(tests_path) / "testsession.local.settings.yml"
    return TestSessionConfiguration.load(settings_file_path)


@pytest.fixture(scope="session")
def measurements(spark: SparkSession, test_files_folder_path: str) -> DataFrame:
    create_database(spark, MeasurementsBronzeDatabase.DATABASE_NAME)

    create_table(
        spark,
        database_name=MeasurementsBronzeDatabase.DATABASE_NAME,
        table_name=MeasurementsBronzeDatabase.MEASUREMENTS_NAME,
        schema=measurements_bronze_v1,
        table_location=f"{MeasurementsBronzeDatabase.DATABASE_NAME}/{MeasurementsBronzeDatabase.MEASUREMENTS_NAME}",
    )

    file_name = f"{test_files_folder_path}/{MeasurementsBronzeDatabase.DATABASE_NAME}-{MeasurementsBronzeDatabase.MEASUREMENTS_NAME}.csv"
    measurements = read_from_csv(spark, file_name)

    return create_measurements_dataframe(spark, measurements)


@pytest.fixture(scope="session")
def seed_gold_table(spark: SparkSession, test_files_folder_path: str) -> None:
    create_database(spark, MeasurementsGoldDatabase.DATABASE_NAME)

    create_table(
        spark,
        database_name=MeasurementsGoldDatabase.DATABASE_NAME,
        table_name=MeasurementsGoldDatabase.TIME_SERIES_POINTS_NAME,
        schema=time_series_points_v1,
        table_location=f"{MeasurementsGoldDatabase.DATABASE_NAME}/{MeasurementsGoldDatabase.TIME_SERIES_POINTS_NAME}",
    )

    file_name = f"{test_files_folder_path}/{MeasurementsGoldDatabase.DATABASE_NAME}-{MeasurementsGoldDatabase.TIME_SERIES_POINTS_NAME}.csv"
    time_series_points = read_from_csv(spark, file_name)
    time_series_points.write.saveAsTable(
        f"{MeasurementsGoldDatabase.DATABASE_NAME}.{MeasurementsGoldDatabase.TIME_SERIES_POINTS_NAME}",
        format="delta",
        mode="overwrite",
    )
