import pyspark.sql.functions as F
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import ArrayType
from testcommon.dataframes import assert_schema

from opengeh_electrical_heating.infrastructure.measurements_bronze.data_structure import MeasurementsBronze
from opengeh_electrical_heating.infrastructure.measurements_bronze.schemas.measurements_bronze_v1 import (
    measurements_bronze_v1,
    point,
)


def create_measurements_bronze_dataframe(spark: SparkSession, measurements: DataFrame) -> MeasurementsBronze:
    measurements = measurements.withColumn(
        "points",
        F.from_json(F.col("points"), ArrayType(point)),
    )

    measurements = (
        measurements.withColumn(
            "start_datetime",
            F.to_timestamp(F.col("start_datetime"), "yyyy-MM-dd HH:mm:ss"),
        )
        .withColumn("end_datetime", F.to_timestamp(F.col("end_datetime"), "yyyy-MM-dd HH:mm:ss"))
        .withColumn(
            "transaction_creation_datetime",
            F.to_timestamp(F.col("transaction_creation_datetime"), "yyyy-MM-dd HH:mm:ss"),
        )
    )

    measurements = spark.createDataFrame(measurements.rdd, schema=measurements_bronze_v1, verifySchema=True)

    assert_schema(measurements.schema, measurements_bronze_v1)

    return MeasurementsBronze(measurements)
