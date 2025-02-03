from pathlib import Path
from unittest import mock

import pytest
from pyspark.sql import SparkSession
from telemetry_logging.logging_configuration import LoggingSettings, configure_logging
from testcommon.dataframes import (
    AssertDataframesConfiguration,
    read_csv,
)
from testcommon.etl import TestCase, TestCases

from contracts.electricity_market__capacity_settlement.metering_point_periods_v1 import (
    metering_point_periods_v1,
)
from contracts.measurements_gold.time_series_points_v1 import (
    time_series_points_v1,
)
from opengeh_capacity_settlement.domain.calculation import (
    execute_core_logic,
)
from tests.scenario_tests.capacity_settlement_test_args import CapacitySettlementTestArgs
from tests.testsession_configuration import (
    TestSessionConfiguration,
)


@pytest.fixture(scope="session", autouse=True)
def enable_logging() -> None:
    """Ensure that logging hooks don't fail due to _TRACER_NAME not being set."""
    env_args = {
        "CLOUD_ROLE_NAME": "test_role",
        "APPLICATIONINSIGHTS_CONNECTION_STRING": "connection_string",
        "SUBSYSTEM": "test_subsystem",
        "ORCHESTRATION_INSTANCE_ID": "4a540892-2c0a-46a9-9257-c4e13051d76b",
    }
    # Command line arguments
    with (
        mock.patch(
            "sys.argv",
            [
                "program_name",
                "--force_configuration",
                "false",
                "--orchestration_instance_id",
                "4a540892-2c0a-46a9-9257-c4e13051d76a",
            ],
        ),
        mock.patch.dict("os.environ", env_args, clear=False),
    ):
        logging_settings = LoggingSettings()
        logging_settings.applicationinsights_connection_string = None  # for testing purposes
        configure_logging(logging_settings=logging_settings, extras=None)


@pytest.fixture(scope="module")
def test_cases(spark: SparkSession, request: pytest.FixtureRequest) -> TestCases:
    """Fixture used for scenario tests. Learn more in package `testcommon.etl`."""

    # Get the path to the scenario
    scenario_path = str(Path(request.module.__file__).parent)

    # Read input data
    time_series_points = read_csv(
        spark,
        f"{scenario_path}/when/measurements_gold/time_series_points_v1.csv",
        time_series_points_v1,
    )
    metering_point_periods = read_csv(
        spark,
        f"{scenario_path}/when/electricity_market__capacity_settlement/metering_point_periods_v1.csv",
        metering_point_periods_v1,
    )

    args = CapacitySettlementTestArgs(f"{scenario_path}/when/job_parameters.env")

    # Execute the logic
    calculation_output = execute_core_logic(
        spark,
        time_series_points,
        metering_point_periods,
        args.calculation_month,
        args.calculation_year,
        args.time_zone,
    )

    # Return test cases
    return TestCases(
        [
            TestCase(
                expected_csv_path=f"{scenario_path}/then/electrical_heating_internal/calculations.csv",
                actual=calculation_output.calculations,
            ),
            TestCase(
                expected_csv_path=f"{scenario_path}/then/measurements.csv",
                actual=calculation_output.measurements,
            ),
        ]
    )


@pytest.fixture(scope="session")
def assert_dataframes_configuration(
    test_session_configuration: TestSessionConfiguration,
) -> AssertDataframesConfiguration:
    return AssertDataframesConfiguration(
        show_actual_and_expected_count=test_session_configuration.scenario_tests.show_actual_and_expected_count,
        show_actual_and_expected=test_session_configuration.scenario_tests.show_actual_and_expected,
        show_columns_when_actual_and_expected_are_equal=test_session_configuration.scenario_tests.show_columns_when_actual_and_expected_are_equal,
    )
