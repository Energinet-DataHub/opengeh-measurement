from pyspark.sql import DataFrame
from pyspark_functions.data_frame_wrapper import DataFrameWrapper

from opengeh_electrical_heating.infrastructure.measurements_bronze.schemas.measurements_bronze_v1 import (
    measurements_bronze_v1,
)


class MeasurementsBronze(DataFrameWrapper):
    """Represents the bronze measurements data structure."""

    def __init__(self, df: DataFrame):
        super().__init__(
            df,
            measurements_bronze_v1,
            # We ignore_nullability because it has turned out to be too hard and even possibly
            # introducing more errors than solving in order to stay in exact sync with the
            # logically correct schema.
            ignore_nullability=True,
        )
