import pyspark.sql.types as T
from pyspark.sql import DataFrame
from pyspark_functions.data_frame_wrapper import DataFrameWrapper


class CalculatedMeasurementsDaily(DataFrameWrapper):
    def __init__(self, df: DataFrame):
        super().__init__(
            df=df,
            schema=calculated_measurements_daily_schema,
            ignore_nullability=True,
        )


calculated_measurements_daily_schema = T.StructType(
    [
        T.StructField("metering_point_id", T.StringType(), False),
        T.StructField("date", T.TimestampType(), False),
        T.StructField("quantity", T.DecimalType(18, 3), False),
    ]
)
