from pyspark.sql import DataFrame
from pyspark_functions.data_frame_wrapper import DataFrameWrapper

from opengeh_electrical_heating.infrastructure.electrical_heating_internal.schemas.calculations import calculations


class Calculations(DataFrameWrapper):
    """Represents the calculations data structure."""

    def __init__(self, df: DataFrame):
        super().__init__(
            df,
            calculations,
            # We ignore_nullability because it has turned out to be too hard and even possibly
            # introducing more errors than solving in order to stay in exact sync with the
            # logically correct schema.
            ignore_nullability=True,
        )
