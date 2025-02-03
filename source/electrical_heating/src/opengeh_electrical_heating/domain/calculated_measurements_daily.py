import pyspark.sql.types as T
from pyspark.sql import DataFrame
from pyspark_functions.data_frame_wrapper import DataFrameWrapper


class CalculatedMeasurementsDaily(DataFrameWrapper):
    def __init__(self, df: DataFrame):
        columns = [field.name for field in calculated_measurements_daily_schema.fields]
        df = df.select(columns)


calculated_measurements_daily_schema = T.StructType(
    [
        T.StructField("metering_point_id", T.StringType(), False),
        T.StructField("date", T.TimestampType(), False),
        T.StructField("quantity", T.DecimalType(), False),
    ]
)
