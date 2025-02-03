import uuid
from typing import Any
from unittest.mock import patch

import pytest
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from opengeh_electrical_heating.application.execute_with_deps import _execute_with_deps
from opengeh_electrical_heating.application.job_args.environment_variables import EnvironmentVariable
from opengeh_electrical_heating.infrastructure.measurements_bronze.database_definitions import (
    MeasurementsBronzeDatabase,
)


@pytest.fixture(scope="session")
def job_environment_variables(test_files_folder_path) -> dict:
    return {
        EnvironmentVariable.CATALOG_NAME.name: "spark_catalog",
        EnvironmentVariable.TIME_ZONE.name: "Europe/Copenhagen",
        EnvironmentVariable.ELECTRICITY_MARKET_DATA_PATH.name: test_files_folder_path,
    }


@pytest.mark.skip(reason="Skipping this until write (results) functionality has been implemented")
def test_execute_with_deps(spark: SparkSession, job_environment_variables: dict, seed_gold_table: Any) -> None:
    # Arrange
    orchestration_instance_id = str(uuid.uuid4())
    sys_argv = ["dummy_script_name", "--orchestration-instance-id", orchestration_instance_id]

    # Act
    with patch("sys.argv", sys_argv):
        with patch.dict("os.environ", job_environment_variables):
            _execute_with_deps()

    # Assert
    actual = spark.read.table(
        f"{MeasurementsBronzeDatabase.DATABASE_NAME}.{MeasurementsBronzeDatabase.MEASUREMENTS_NAME}"
    ).where(F.col("orchestration_instance_id") == orchestration_instance_id)
    assert actual.count() > 0
