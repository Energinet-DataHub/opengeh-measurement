from typing import Optional

from pyspark.sql import DataFrame, SparkSession

from opengeh_gold.application.ports.silver_port import SilverPort
from opengeh_gold.infrastructure.config.database_names import DatabaseNames
from opengeh_gold.infrastructure.shared_helpers import get_full_table_name


class DeltaSilverAdapter(SilverPort):
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def read_stream(self, table_name: str, read_options: Optional[dict] = None) -> DataFrame:
        return (
            self.spark.readStream.format("delta")
            .options(**read_options or {})
            .table(get_full_table_name(DatabaseNames.silver, table_name))
        )
