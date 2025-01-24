import os

from spark_sql_migrations import (
    SparkSqlMigrationsConfiguration,
    create_and_configure_container,
    migration_pipeline,
)

import silver.migrations.substitutions as substitutions
from silver.infrastructure.utils.env_vars_utils import get_catalog_name
from silver.migrations.database_names import DatabaseNames
from silver.migrations.table_names import TableNames


def migrate() -> None:
    _configure_spark_sql_migrations()
    migration_pipeline.migrate()


def _configure_spark_sql_migrations() -> None:
    substitution_variables = substitutions.substitutions()
    catalog_name = get_catalog_name()

    spark_config = SparkSqlMigrationsConfiguration(
        migration_schema_name=DatabaseNames.silver_database,
        migration_table_name=TableNames.executed_migrations_table,
        migration_scripts_folder_path="silver.migrations.migration_scripts",
        substitution_variables=substitution_variables,
        catalog_name=catalog_name,
    )

    create_and_configure_container(spark_config)
