import testcommon.dataframes.assert_schemas as assert_schemas
from pyspark.sql import SparkSession

from opengeh_gold.domain.schemas.gold_measurements import (
    gold_measurements_schema,
)
from opengeh_gold.infrastructure.config.database_names import DatabaseNames
from opengeh_gold.infrastructure.config.table_names import TableNames


def test__migrations__should_create_gold_measurements(spark: SparkSession, migrations_executed):
    # Assert
    gold_measurements = spark.table(f"{DatabaseNames.gold}.{TableNames.gold_measurements}")
    assert_schemas.assert_schema(actual=gold_measurements.schema, expected=gold_measurements_schema)
