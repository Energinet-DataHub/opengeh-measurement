from pyspark.sql import DataFrame, SparkSession

from opengeh_electrical_heating.infrastructure.measurements_gold.data_structure import TimeSeriesPoints
from opengeh_electrical_heating.infrastructure.measurements_gold.database_definitions import (
    MeasurementsGoldDatabase,
)


class Repository:
    def __init__(
        self,
        spark: SparkSession,
        catalog_name: str,
    ) -> None:
        self._spark = spark
        self._catalog_name = catalog_name

    def read_time_series_points(self) -> TimeSeriesPoints:
        df = self._read_view_or_table(
            MeasurementsGoldDatabase.TIME_SERIES_POINTS_NAME,
        )
        return TimeSeriesPoints(df)

    def _read_view_or_table(
        self,
        table_name: str,
    ) -> DataFrame:
        name = f"{self._catalog_name}.{MeasurementsGoldDatabase.DATABASE_NAME}.{table_name}"
        return self._spark.read.format("delta").table(name)
