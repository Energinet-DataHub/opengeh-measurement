from pyspark.sql import DataFrame, SparkSession

from opengeh_electrical_heating.infrastructure.measurements_gold.database_definitions import (
    MeasurementsGoldDatabase,
)
from opengeh_electrical_heating.infrastructure.measurements_gold.schemas.time_series_points_v1 import (
    time_series_points_v1,
)


class Repository:
    def __init__(
        self,
        spark: SparkSession,
        catalog_name: str,
    ) -> None:
        self._spark = spark
        self._catalog_name = catalog_name

    def read_time_series_points(self) -> DataFrame:
        # TODO The table time series points is not yet available in the gold database or renamed.
        return self._spark.createDataFrame([], schema=time_series_points_v1)
        # return self._read_view_or_table(MeasurementsGoldDatabase.TIME_SERIES_POINTS_NAME)        )

    def _read_view_or_table(
        self,
        table_name: str,
    ) -> DataFrame:
        name = f"{self._catalog_name}.{MeasurementsGoldDatabase.DATABASE_NAME}.{table_name}"
        return self._spark.read.format("delta").table(name)
