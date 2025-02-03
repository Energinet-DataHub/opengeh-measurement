import pyspark.sql.functions as F
from pyspark.sql import DataFrame
from pyspark.sql.protobuf.functions import from_protobuf, to_protobuf

import opengeh_bronze.infrastructure.helpers.path_helper as path_helper
from opengeh_bronze.domain.constants.column_names.bronze_submitted_transactions_column_names import (
    BronzeSubmittedTransactionsColumnNames,
    ValueColumnNames,
)

alias_name = "measurement"


def transform(submitted_transactions: DataFrame) -> DataFrame:
    unpacked_submitted_transactions = unpack_submitted_transactions(submitted_transactions)
    return unpacked_submitted_transactions.transform(prepare_measurement).transform(pack_proto)


def prepare_measurement(df):
    return df.withColumn(
        BronzeSubmittedTransactionsColumnNames.value,
        F.struct(
            df[ValueColumnNames.version].alias(ValueColumnNames.version),
            df[ValueColumnNames.orchestration_instance_id].alias(ValueColumnNames.orchestration_instance_id),
            df[ValueColumnNames.orchestration_type].alias(ValueColumnNames.orchestration_type),
        ),
    )


def pack_proto(df) -> DataFrame:
    descriptor_path = path_helper.get_protobuf_descriptor_path("submitted_transaction_persisted.binpb")
    message_name = "SubmittedTransactionPersisted"
    return df.withColumn("body", to_protobuf(df.value, message_name, descFilePath=descriptor_path))


def unpack_submitted_transactions(bronze_measurements: DataFrame) -> DataFrame:
    """Unpacks the protobuf message and maps the fields to the correct columns."""
    return bronze_measurements.transform(unpack_proto).transform(map_message)


def unpack_proto(df):
    descriptor_path = path_helper.get_protobuf_descriptor_path("persist_submitted_transaction.binpb")
    message_name = "PersistSubmittedTransaction"
    return df.select(from_protobuf(df.value, message_name, descFilePath=descriptor_path).alias(alias_name))


def map_message(df):
    return df.select(
        f"{alias_name}.{ValueColumnNames.version}",
        f"{alias_name}.{ValueColumnNames.orchestration_instance_id}",
        f"{alias_name}.{ValueColumnNames.orchestration_type}",
    )
