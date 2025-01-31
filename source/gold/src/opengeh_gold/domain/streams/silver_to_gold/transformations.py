from datetime import timedelta

import pyspark.sql.functions as F
from pyspark.sql import Column, DataFrame
from pyspark.sql.types import TimestampType

from opengeh_gold.domain.constants.column_names.gold_measurements_column_names import (
    GoldMeasurementsColumnNames,
)
from opengeh_gold.domain.constants.column_names.silver_measurements_column_names import (
    SilverMeasurementsColumnNames,
)
from opengeh_gold.domain.constants.enums.resolutions import ResolutionEnum


def transform_silver_to_gold(df: DataFrame) -> DataFrame:
    exploded_df = explode_silver_points(df)

    return exploded_df.select(
        F.col(SilverMeasurementsColumnNames.metering_point_id).alias(GoldMeasurementsColumnNames.metering_point_id),
        (
            # When monthly resolution
            F.when(
                F.col(SilverMeasurementsColumnNames.resolution) == ResolutionEnum.P1M.value,
                _get_monthly_observation_time().cast(TimestampType()),
            )
            # When 15 minutes resolution
            .when(
                F.col(SilverMeasurementsColumnNames.resolution) == ResolutionEnum.PT15M.value,
                _get_15_minutes_observation_time().cast(TimestampType()),
            )
            # When hourly resolution
            .when(
                F.col(SilverMeasurementsColumnNames.resolution) == ResolutionEnum.PT1H.value,
                _get_hourly_observation_time().cast(TimestampType()),
            )
            .otherwise(F.col(SilverMeasurementsColumnNames.start_datetime))
        ).alias(GoldMeasurementsColumnNames.observation_time),
        F.col(f"col.{SilverMeasurementsColumnNames.Points.quantity}").alias(GoldMeasurementsColumnNames.quantity),
        F.col(f"col.{SilverMeasurementsColumnNames.Points.quality}").alias(GoldMeasurementsColumnNames.quality),
        F.col(SilverMeasurementsColumnNames.metering_point_type).alias(GoldMeasurementsColumnNames.metering_point_type),
        F.col(SilverMeasurementsColumnNames.transaction_id).alias(GoldMeasurementsColumnNames.transaction_id),
        F.col(SilverMeasurementsColumnNames.transaction_creation_datetime).alias(
            GoldMeasurementsColumnNames.transaction_creation_datetime
        ),
        F.current_timestamp().alias(GoldMeasurementsColumnNames.created),
        F.current_timestamp().alias(GoldMeasurementsColumnNames.modified),
    )


def explode_silver_points(df: DataFrame) -> DataFrame:
    return df.select("*", F.explode(F.col(SilverMeasurementsColumnNames.points))).drop(
        SilverMeasurementsColumnNames.points
    )


def _get_monthly_observation_time() -> Column:
    # When start_datetime = first day of month, add month based on its position value
    return (
        F.when(
            F.dayofmonth(F.col(SilverMeasurementsColumnNames.start_datetime)) == F.lit(1),
            F.expr("add_months(start_datetime, (col.position - 1))"),
        )
        # Otherwise when not first of month
        .otherwise(
            # When first position => do nothing
            F.when(
                F.col(f"col.{SilverMeasurementsColumnNames.Points.position}") == F.lit(1),
                F.col(SilverMeasurementsColumnNames.start_datetime),
            ).otherwise(
                # Otherwise add months based on its position value
                F.expr("add_months(date_trunc('mon', start_datetime), (col.position - 1))")
            )
        )
    )


def _get_15_minutes_observation_time() -> Column:
    return F.unix_timestamp(F.col(SilverMeasurementsColumnNames.start_datetime)) + (
        (F.col(f"col.{SilverMeasurementsColumnNames.Points.position}") - F.lit(1))
        * F.lit(timedelta(minutes=15).seconds)
    )


def _get_hourly_observation_time() -> Column:
    return F.unix_timestamp(F.col(SilverMeasurementsColumnNames.start_datetime)) + (
        (F.col(f"col.{SilverMeasurementsColumnNames.Points.position}") - F.lit(1)) * F.lit(timedelta(hours=1).seconds)
    )
