from telemetry_logging import Logger, logging_configuration
from telemetry_logging.decorators import start_trace

from opengeh_electrical_heating.application.execute_with_deps import (
    _execute_with_deps,
)
from opengeh_electrical_heating.application.job_args.electrical_heating_args import ElectricalHeatingArgs
from opengeh_electrical_heating.infrastructure.spark_initializor import (
    initialize_spark,
)


def execute() -> None:
    electrical_heating_args = ElectricalHeatingArgs()  # Retrieve calculation oriented settings / job arguments
    logging_settings = logging_configuration.LoggingSettings(
        subsystem="measurements", cloud_role_name="dbr-electrical-heating"
    )  # Retrieve logging oriented settings
    logging_configuration.configure_logging(logging_settings=logging_settings)
    # Add another extra (added to all logging messages as properties)
    logging_configuration.add_extras({"subsystem": "measurements"})
    # Execute the application
    orchestrate_business_logic(job_arguments=electrical_heating_args, logging_settings=logging_settings)


@start_trace(
    initial_span_name="orchestrate_business_logic"
)  # Wraps the execute_with_deps function that starts the opentelemetry tracer and starts an initial span named using the name of the decorated function, or specifically provided name with initial_span_name
def orchestrate_business_logic(
    job_arguments: ElectricalHeatingArgs, logging_settings: logging_configuration.LoggingSettings
) -> None:
    logger = Logger(__name__)
    logger.info(f"Command line arguments / env variables retrieved for Logging Settings: {logging_settings}")
    logger.info(f"Command line arguments retrieved for electrical heating job Oriented Parameters: {job_arguments}")
    spark = initialize_spark()
    _execute_with_deps(spark, args=job_arguments)
