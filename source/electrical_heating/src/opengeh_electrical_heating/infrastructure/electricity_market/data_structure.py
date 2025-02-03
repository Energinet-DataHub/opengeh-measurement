from pyspark.sql import DataFrame
from pyspark_functions.data_frame_wrapper import DataFrameWrapper

from opengeh_electrical_heating.infrastructure.electricity_market.schemas.child_metering_points_v1 import (
    child_metering_points_v1,
)
from opengeh_electrical_heating.infrastructure.electricity_market.schemas.consumption_metering_point_periods_v1 import (
    consumption_metering_point_periods_v1,
)


class ConsumptionMeteringPointPeriods(DataFrameWrapper):
    """Represents the consumption metering point periods data structure."""

    def __init__(self, df: DataFrame):
        super().__init__(
            df,
            consumption_metering_point_periods_v1,
            # We ignore_nullability because it has turned out to be too hard and even possibly
            # introducing more errors than solving in order to stay in exact sync with the
            # logically correct schema.
            ignore_nullability=True,
        )


class ChildMeteringPoints(DataFrameWrapper):
    """Represents the child metering points data structure."""

    def __init__(self, df: DataFrame):
        super().__init__(
            df,
            child_metering_points_v1,
            # We ignore_nullability because it has turned out to be too hard and even possibly
            # introducing more errors than solving in order to stay in exact sync with the
            # logically correct schema.
            ignore_nullability=True,
        )
