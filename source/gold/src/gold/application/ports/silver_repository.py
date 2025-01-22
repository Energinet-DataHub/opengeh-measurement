﻿from abc import ABC, abstractmethod
from typing import Optional

from pyspark.sql import DataFrame


class SilverRepository(ABC):
    @abstractmethod
    def read_stream(self, table_name, read_options: Optional[dict] = None) -> DataFrame:
        """
        Reads a streaming DataFrame from a Delta table in the Silver layer.

        Args:
            table_name (str): The name of the Delta table to read from.
            read_options (Optional[dict], optional): Optional configurations for reading the stream.

        Returns:
            DataFrame: A Spark DataFrame representing the streaming data from the specified Delta table.
        """
        pass
