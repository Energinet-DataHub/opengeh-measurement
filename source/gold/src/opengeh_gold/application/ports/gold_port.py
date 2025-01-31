from abc import ABC, abstractmethod
from typing import Callable

from pyspark.sql import DataFrame


class GoldPort(ABC):
    @abstractmethod
    def start_write_stream(
        self,
        df_source_stream: DataFrame,
        query_name: str,
        table_name: str,
        batch_operation: Callable[["DataFrame", int], None],
        terminate_on_empty: bool = False,
    ) -> None:
        """Start a streaming write operation to a Gold Delta table with the specified configurations.

        Args:
            df_source_stream (DataFrame): The source streaming DataFrame to be written.
            query_name (str): The name of the streaming query.
            table_name (str): The name of the Gold table to write to, used to create a checkpoint path.
            batch_operation (Callable[[DataFrame, int], None]): A callable that processes each micro-batch.
            terminate_on_empty (bool, optional): Whether the stream should stop when no more data is currently available.
                Defaults to False.
        """

    @abstractmethod
    def append(self, df: DataFrame, table_name: str) -> None:
        """Append a static DataFrame to a Delta table.

        Args:
            df (DataFrame): The DataFrame to append to the Delta table.
            table_name (str): The name of the Delta table to append to.
        """
