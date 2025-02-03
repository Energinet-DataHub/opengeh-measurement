"""Entry point for the capacity-settlement application."""

from telemetry_logging import logging_configuration
from telemetry_logging.decorators import start_trace
from telemetry_logging.logger import Logger

from opengeh_capacity_settlement.application.execute_with_deps import _execute_with_deps
from opengeh_capacity_settlement.application.job_args.capacity_settlement_args import CapacitySettlementArgs


def execute() -> None:
    electrical_heating_args = CapacitySettlementArgs()  # Retrieve calculation oriented settings / job arguments
    logging_settings = logging_configuration.LoggingSettings(
        subsystem="measurements", cloud_role_name="dbr-capacity-settlement"
    )
    logging_configuration.configure_logging(logging_settings=logging_settings)
    # Add another extra (added to all logging events as properties)
    logging_configuration.add_extras({"subsystem": "measurements"})
    # Execute the application
    orchestrate_business_logic(job_arguments=electrical_heating_args, logging_settings=logging_settings)


@start_trace(
    initial_span_name="capacity-settlement-job"
)  # Wraps orchestrate_business_logic with start_trace: starting a tracer, and provides an initial span with name initial_span_name
def orchestrate_business_logic(
    job_arguments: CapacitySettlementArgs, logging_settings: logging_configuration.LoggingSettings
) -> None:
    logger = Logger(__name__)
    logger.info(f"Command line arguments / env variables retrieved for Logging Settings: {logging_settings}")
    logger.info(f"Command line arguments retrieved for electrical heating job Oriented Parameters: {job_arguments}")
    _execute_with_deps(job_arguments=job_arguments)
