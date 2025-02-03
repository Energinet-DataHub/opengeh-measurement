from pyspark.sql.types import (
    BinaryType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from opengeh_bronze.domain.constants.column_names.notify_transactions_persisted_event_column_names import (
    NotifyTransactionsPersistedEventColumnNames,
)

notify_transactions_persisted_event = StructType(
    [
        StructField(NotifyTransactionsPersistedEventColumnNames.key, BinaryType(), True),
        StructField(NotifyTransactionsPersistedEventColumnNames.value, BinaryType(), True),
        StructField(NotifyTransactionsPersistedEventColumnNames.topic, StringType(), True),
        StructField(NotifyTransactionsPersistedEventColumnNames.partition, IntegerType(), True),
    ]
)
