from pyspark.sql import DataFrame, SparkSession

from opengeh_bronze.domain.constants.database_names import DatabaseNames
from opengeh_bronze.domain.constants.table_names import TableNames


class BronzeRepository:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def read_measurements(self) -> DataFrame:
        return self.spark.readStream.format("delta").table(
            f"{DatabaseNames.bronze_database}.{TableNames.bronze_measurements_table}"
        )

    def read_submitted_transactions(self) -> DataFrame:
        return self.spark.readStream.format("delta").table(
            f"{DatabaseNames.bronze_database}.{TableNames.bronze_submitted_transactions_table}"
        )
