﻿from pyspark.sql import DataFrame, SparkSession
from electrical_heating.infrastructure.measurements_bronze.repository import Repository


def test__write_measurements__can_be_read(
    spark: SparkSession,
    measurements_dataframe: DataFrame,
    default_catalog: str,
) -> None:
    # Arrange
    repository = Repository(spark, default_catalog)
    excepted_count = measurements_dataframe.count()

    # Act
    repository.write_measurements(measurements_dataframe)

    # Assert
    assert repository.read_measurements().count() == excepted_count
