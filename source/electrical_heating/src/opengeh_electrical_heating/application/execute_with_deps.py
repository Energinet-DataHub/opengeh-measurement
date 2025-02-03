"""A module."""

import uuid
from datetime import datetime, timezone

from pyspark.sql import DataFrame, SparkSession
from telemetry_logging import use_span

import opengeh_electrical_heating.infrastructure.electrical_heating_internal as ehi
import opengeh_electrical_heating.infrastructure.electricity_market as em
import opengeh_electrical_heating.infrastructure.measurements_gold as mg
from opengeh_electrical_heating.application.job_args.electrical_heating_args import (
    ElectricalHeatingArgs,
)
from opengeh_electrical_heating.domain import ColumnNames
from opengeh_electrical_heating.domain.calculation import (
    execute_core_logic,
)
from opengeh_electrical_heating.domain.calculation_results import (
    CalculationOutput,
)
from opengeh_electrical_heating.infrastructure.electrical_heating_internal.schemas import (
    calculations as schemas,
)


@use_span()
def _execute_with_deps(spark: SparkSession, args: ElectricalHeatingArgs) -> None:
    if args.execution_start_datetime is not None:
        execution_start_datetime = datetime.now(timezone.utc)

    # Create repositories to obtain data frames
    electricity_market_repository = em.Repository(spark, args.electricity_market_data_path)
    measurements_gold_repository = mg.Repository(spark, args.catalog_name)
    electrical_heating_internal_repository = ehi.Repository(spark, args.catalog_name)

    # Read data frames
    time_series_points = measurements_gold_repository.read_time_series_points()

    consumption_metering_point_periods = electricity_market_repository.read_consumption_metering_point_periods()

    child_metering_point_periods = electricity_market_repository.read_child_metering_points()

    calculation_output = execute_calculation(
        spark,
        time_series_points,
        consumption_metering_point_periods,
        child_metering_point_periods,
        args,
        execution_start_datetime,
    )

    electrical_heating_internal_repository.save(calculation_output.calculations)


def execute_calculation(
    spark: SparkSession,
    time_series_points: DataFrame,
    consumption_metering_point_periods: DataFrame,
    child_metering_point_periods: DataFrame,
    args: ElectricalHeatingArgs,
    execution_start_datetime: datetime,
) -> CalculationOutput:
    measurements = execute_core_logic(
        time_series_points,
        consumption_metering_point_periods,
        child_metering_point_periods,
        args.time_zone,
    )

    calculations = create_calculation(
        spark,
        args.orchestration_instance_id,
        execution_start_datetime,
        datetime.now(timezone.utc),
    )

    return CalculationOutput(measurements=measurements, calculations=calculations)


def create_calculation(
    spark: SparkSession,
    orchestration_instance_id: uuid.UUID,
    execution_start_datetime: datetime,
    execution_stop_datetime: datetime,
) -> DataFrame:
    # TODO Temp. calculation id - refac when calculation id is available
    calculation_id = str(uuid.uuid4())

    data = [
        {
            ColumnNames.calculation_id: calculation_id,
            ColumnNames.orchestration_instance_id: str(orchestration_instance_id),
            ColumnNames.execution_start_datetime: execution_start_datetime,
            ColumnNames.execution_stop_datetime: execution_stop_datetime,
        }
    ]

    return spark.createDataFrame(data, schemas.calculations)
