﻿import database_migration.substitutions as substitutions
import os
from database_migration.constants.database_constants import DatabaseConstants
from database_migration.constants.table_constants import TableConstants
from spark_sql_migrations import (
    migration_pipeline,
    SparkSqlMigrationsConfiguration,
    create_and_configure_container
)


def migrate() -> None:
    _configure_spark_sql_migrations()
    migration_pipeline.migrate()


def _configure_spark_sql_migrations() -> None:
    substitution_variables = substitutions.substitutions()
    catalog_name = os.environ["CATALOG_NAME"]

    spark_config = SparkSqlMigrationsConfiguration(
        migration_schema_name=DatabaseConstants.migrations_database,
        migration_table_name=TableConstants.executed_migrations_table,
        migration_scripts_folder_path="database_migration.migration_scripts",
        substitution_variables=substitution_variables,
        catalog_name=catalog_name
    )

    create_and_configure_container(spark_config)
