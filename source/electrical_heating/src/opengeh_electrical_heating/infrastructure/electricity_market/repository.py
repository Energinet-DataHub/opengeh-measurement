from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T
from testcommon.dataframes import read_csv

from opengeh_electrical_heating.infrastructure.electricity_market.schemas.child_metering_points_v1 import (
    child_metering_points_v1,
)
from opengeh_electrical_heating.infrastructure.electricity_market.schemas.consumption_metering_point_periods_v1 import (
    consumption_metering_point_periods_v1,
)


class Repository:
    def __init__(
        self,
        spark: SparkSession,
        electricity_market_data_path: str,
    ) -> None:
        self._spark = spark
        self._electricity_market_data_path = electricity_market_data_path

    def read_consumption_metering_point_periods(self) -> DataFrame:
        file_path = f"{self._electricity_market_data_path}/consumption_metering_point_periods_v1.csv"
        return read_csv(spark=self._spark, path=file_path, schema=consumption_metering_point_periods_v1)

    def read_child_metering_points(self) -> DataFrame:
        file_path = f"{self._electricity_market_data_path}/child_metering_points_v1.csv"
        return read_csv(spark=self._spark, path=file_path, schema=child_metering_points_v1)


# TODO JMG: Use read_csv from opengeh_python_packages
def _read_csv2(
    spark: SparkSession,
    path: str,
    schema: T.StructType,
    sep: str = ";",
    ignored_value="[IGNORED]",
) -> DataFrame:
    """Read a CSV file into a Spark DataFrame.

    Args:
        spark (SparkSession): The Spark session.
        path (str): The path to the CSV file.
        schema (StructType): The schema of the CSV file.
        sep (str, optional): The separator of the CSV file. Defaults to ";".
        ignored_value (str, optional): Columns where all rows is equal to the
            ignored_value will be removed from the resulting DataFrame.
            Defaults to "[IGNORED]".

    Returns:
        DataFrame: The Spark DataFrame.
    """
    raw_df = spark.read.csv(path, header=True, sep=sep)

    # Check each column to see if all values are "[IGNORED]"
    ignore_check = raw_df.agg(*[F.every(F.col(c) == F.lit(ignored_value)).alias(c) for c in raw_df.columns]).collect()

    # Get the columns that should be ignored
    ignored_cols = [c for c, v in ignore_check[0].asDict().items() if v and c in schema.fieldNames()]

    raw_df = raw_df.drop(*ignored_cols)

    transforms = []
    for field in schema.fields:
        if field.name in raw_df.columns:
            if isinstance(field.dataType, T.ArrayType):
                transforms.append(F.from_json(F.col(field.name), field.dataType).alias(field.name))
            else:
                transforms.append(F.col(field.name).cast(field.dataType).alias(field.name))

    df = raw_df.select(*transforms)
    return spark.createDataFrame(df.rdd, schema=schema, verifySchema=True)
