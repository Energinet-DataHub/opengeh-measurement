from pyspark.sql import SparkSession

from opengeh_bronze.domain.schemas.submitted_transactions import submitted_transactions_schema


class SubmittedTransactionsBuilder:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.data = []

    def add_row(
        self, key=None, value=None, topic=None, partition=None, offset=None, timestamp=None, timestampType=None
    ) -> "SubmittedTransactionsBuilder":
        self.data.append((key, value, topic, partition, offset, timestamp, timestampType))

        return self

    def build(self):
        return self.spark.createDataFrame(self.data, schema=submitted_transactions_schema)
