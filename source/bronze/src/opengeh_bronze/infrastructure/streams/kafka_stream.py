from pyspark.sql import DataFrame, SparkSession

import opengeh_bronze.infrastructure.shared_helpers as shared_helpers
from opengeh_bronze.domain.constants.database_names import DatabaseNames
from opengeh_bronze.domain.constants.table_names import TableNames
from opengeh_bronze.infrastructure.config.storage_container_names import StorageContainerNames
from opengeh_bronze.infrastructure.settings.storage_account_settings import (
    StorageAccountSettings,
)
from opengeh_bronze.infrastructure.settings.submitted_transactions_stream_settings import (
    SubmittedTransactionsStreamSettings,
)


class KafkaStream:
    kafka_options: dict

    def __init__(self) -> None:
        self.kafka_options = SubmittedTransactionsStreamSettings().create_kafka_options()

    def submit_transactions(self, spark: SparkSession) -> None:
        checkpoint_location = shared_helpers.get_checkpoint_path(
            StorageAccountSettings().DATALAKE_STORAGE_ACCOUNT, StorageContainerNames.bronze, "submitted_transactions"
        )
        spark.readStream.format("kafka").options(**self.kafka_options).load().writeStream.outputMode("append").trigger(
            availableNow=True
        ).option("checkpointLocation", checkpoint_location).toTable(
            f"{DatabaseNames.bronze_database}.{TableNames.bronze_submitted_transactions_table}"
        )

    def write_stream(
        self,
        dataframe: DataFrame,
    ):
        checkpoint_location = shared_helpers.get_checkpoint_path(
            StorageAccountSettings().DATALAKE_STORAGE_ACCOUNT, StorageContainerNames.bronze, "processed_transactions"
        )
        event_hub_namespace = SubmittedTransactionsStreamSettings().event_hub_namespace

        dataframe.writeStream.format("kafka").option("topic", event_hub_namespace).options(**self.kafka_options).option(
            "checkpointLocation", checkpoint_location
        ).trigger(availableNow=True).start()
