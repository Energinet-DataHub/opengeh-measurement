from pyspark.sql.dataframe import DataFrame

from opengeh_gold.application.ports.gold_port import GoldPort
from opengeh_gold.application.ports.silver_port import SilverPort
from opengeh_gold.domain.streams.silver_to_gold.transformations import transform_silver_to_gold


class StreamProcessorMeasurements:
    def __init__(self, silver_port: SilverPort, silver_target_table: str, gold_port: GoldPort, gold_target_table: str):
        self.silver_port = silver_port
        self.silver_target_table = silver_target_table
        self.gold_port = gold_port
        self.gold_target_table = gold_target_table
        self.query_name = "measurements_silver_to_gold"

    def stream_measurements_silver_to_gold(self) -> None:
        df_silver_stream = self.silver_port.read_stream(self.silver_target_table, {"ignoreDeletes": "true"})
        self.gold_port.start_write_stream(
            df_silver_stream, self.query_name, self.gold_target_table, self.pipeline_measurements_silver_to_gold
        )

    def pipeline_measurements_silver_to_gold(self, df_silver: DataFrame, batch_id: int) -> None:
        df_gold = transform_silver_to_gold(df_silver)
        self.gold_port.append(df_gold, self.gold_target_table)
