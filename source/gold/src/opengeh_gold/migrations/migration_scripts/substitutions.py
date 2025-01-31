from opengeh_gold.infrastructure.config.database_names import DatabaseNames
from opengeh_gold.infrastructure.config.table_names import TableNames


def substitutions() -> dict[str, str]:
    return {
        "{gold_database}": DatabaseNames.gold,
        "{gold_measurements}": TableNames.gold_measurements,
    }
