from pyspark.sql import DataFrame, SparkSession

from opengeh_electrical_heating.infrastructure.measurements_bronze.database_definitions import (
    MeasurementsBronzeDatabase,
)


class Repository:
    def __init__(
        self,
        spark: SparkSession,
        catalog_name: str | None = None,
    ) -> None:
        self._spark = spark
        self._database_name = MeasurementsBronzeDatabase.DATABASE_NAME
        self._measurements_table_name = MeasurementsBronzeDatabase.MEASUREMENTS_NAME
        self._catalog_name = catalog_name
        if self._catalog_name:
            self._full_table_path = f"{self._catalog_name}.{self._database_name}.{self._measurements_table_name}"
        else:
            self._full_table_path = f"{self._database_name}.{self._measurements_table_name}"

    def write_measurements(self, df: DataFrame, write_mode: str = "append") -> None:
        df.write.format("delta").mode(write_mode).saveAsTable(self._full_table_path)

    def read_measurements(self) -> DataFrame:
        return self._spark.read.table(self._full_table_path)
