﻿import testcommon.dataframes.assert_schemas as assert_schemas
from pyspark.sql import SparkSession

from bronze.domain.schemas.bronze_measurements import (
    bronze_measurements_schema,
)
from bronze.infrastructure.config.database_names import DatabaseNames
from bronze.infrastructure.config.table_names import TableNames


def test__migrations__should_create_bronze_measurements_table(spark: SparkSession, migrate):
    # Assert
    bronze_measurements = spark.table(f"{DatabaseNames.bronze_database}.{TableNames.bronze_measurements_table}")
    assert_schemas.assert_schema(actual=bronze_measurements.schema, expected=bronze_measurements_schema)
