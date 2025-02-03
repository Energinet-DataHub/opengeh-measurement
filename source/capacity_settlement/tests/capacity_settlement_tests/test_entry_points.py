from unittest import mock

from opengeh_capacity_settlement import entry_point


def test__execute() -> None:
    env_args = {
        "CLOUD_ROLE_NAME": "test_role",
        "APPLICATIONINSIGHTS_CONNECTION_STRING": "connection_string",
        "SUBSYSTEM": "test_subsystem",
        "CATALOG_NAME": "default_hadoop",
        "time_zone": "Europe/Copenhagen",
        "execution_start_datetime": "2019-12-04",
        "calculation_month": "12",
        "calculation_year": "2024",
    }
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
        mock.patch("opengeh_capacity_settlement.entry_point.CapacitySettlementArgs") as mock_CapacitySettlementArgs,
        mock.patch("telemetry_logging.logging_configuration.LoggingSettings") as mock_logging_settings,
        mock.patch("telemetry_logging.logging_configuration.configure_logging") as mock_configure_logging,
        mock.patch("telemetry_logging.logging_configuration.add_extras") as mock_add_extras,
        mock.patch(
            "opengeh_capacity_settlement.entry_point.orchestrate_business_logic"
        ) as mock_orchestrate_business_logic,
    ):
        # Prepare
        expected_subsystem_name = "measurements"

        # Act
        entry_point.execute()

        # assert
        mock_CapacitySettlementArgs.assert_called_once()
        mock_logging_settings.assert_called_once()
        mock_configure_logging.assert_called_once_with(logging_settings=mock_logging_settings.return_value)
        mock_add_extras.assert_called_once_with({"subsystem": expected_subsystem_name})
        mock_orchestrate_business_logic.assert_called_once()  # Patching/mocking this function forces the function not to run
