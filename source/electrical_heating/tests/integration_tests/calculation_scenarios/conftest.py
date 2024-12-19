﻿from pathlib import Path

import pytest
from pyspark.sql import SparkSession
from testcommon.etl import read_csv

from electrical_heating.domain.calculation import execute_core_logic
from electrical_heating.infrastructure.electrical_heating_internal.schemas.calculations import (
    calculations,
)
from electrical_heating.infrastructure.electricity_market.schemas.child_metering_point_periods_v1 import (
    child_metering_point_periods_v1,
)
from electrical_heating.infrastructure.electricity_market.schemas.consumption_metering_point_periods_v1 import (
    consumption_metering_point_periods_v1,
)
from electrical_heating.infrastructure.measurements_gold.schemas.time_series_points_v1 import (
    time_series_points_v1,
)
from tests.integration_tests.calculation_scenarios.temp_testcommon import (
    TestCases,
    TestCase,
)


@pytest.fixture(scope="module")
def test_cases(spark: SparkSession, request) -> TestCases:
    scenario_path = str(Path(request.module.__file__).parent)

    # Read input data
    time_series_points = read_csv(
        spark,
        f"{scenario_path}/when/measurements_gold/time_series_points_v1.csv",
        time_series_points_v1,
    )
    consumption_metering_point_periods = read_csv(
        spark,
        f"{scenario_path}/when/electricity_market__electrical_heating/consumption_metering_point_periods_v1.csv",
        consumption_metering_point_periods_v1,
    )
    child_metering_point_periods = read_csv(
        spark,
        f"{scenario_path}/when/electricity_market__electrical_heating/child_metering_point_periods_v1.csv",
        child_metering_point_periods_v1,
    )

    # Execute the calculation logic
    actual_measurements = execute_core_logic(
        time_series_points,
        consumption_metering_point_periods,
        child_metering_point_periods,
        "Europe/Copenhagen",
    )

    # Read expected data
    test_cases = []

    if Path(f"{scenario_path}/then/measurements.csv").exists():
        expected_measurements = read_csv(
            spark, f"{scenario_path}/then/measurements.csv", actual_measurements.schema
        )
        test_cases.append(
            TestCase(
                name="measurements",
                actual=actual_measurements,
                expected=expected_measurements,
            )
        )

    if Path(
        f"{scenario_path}/then/electrical_heating_internal/calculations.csv"
    ).exists():
        expected_calculations = read_csv(
            spark,
            f"{scenario_path}/then/electrical_heating_internal/calculations.csv",
            calculations,
        )
        test_cases.append(
            TestCase(
                name="calculations",
                # TODO: This must be output from the calculation logic
                actual=spark.createDataFrame([], calculations),
                expected=expected_calculations,
            )
        )

    # Return test cases
    return TestCases(test_cases)
