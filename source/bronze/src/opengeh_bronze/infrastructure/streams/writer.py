from typing import Callable

from pyspark.sql import DataFrame


def write_stream(
    df_source_stream: DataFrame,
    query_name: str,
    options: dict[str, str],
    batch_operation: Callable[["DataFrame", int], None],
) -> None:
    df_source_stream.writeStream.format("delta").queryName(query_name).options(**options).foreachBatch(
        batch_operation
    ).trigger(availableNow=True).start().awaitTermination()
