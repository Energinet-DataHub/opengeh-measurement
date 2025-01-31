from pyspark.sql.types import (
    ArrayType,
    DecimalType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

from opengeh_gold.domain.constants.column_names.silver_measurements_column_names import (
    SilverMeasurementsColumnNames,
)

silver_measurements_schema = StructType(
    [
        StructField(SilverMeasurementsColumnNames.orchestration_type, StringType(), True),
        StructField(SilverMeasurementsColumnNames.orchestration_instance_id, StringType(), True),
        StructField(SilverMeasurementsColumnNames.metering_point_id, StringType(), True),
        StructField(SilverMeasurementsColumnNames.transaction_id, StringType(), True),
        StructField(SilverMeasurementsColumnNames.transaction_creation_datetime, TimestampType(), True),
        StructField(SilverMeasurementsColumnNames.metering_point_type, StringType(), True),
        StructField(SilverMeasurementsColumnNames.product, StringType(), True),
        StructField(SilverMeasurementsColumnNames.unit, StringType(), True),
        StructField(SilverMeasurementsColumnNames.resolution, StringType(), True),
        StructField(SilverMeasurementsColumnNames.start_datetime, TimestampType(), True),
        StructField(SilverMeasurementsColumnNames.end_datetime, TimestampType(), True),
        StructField(
            SilverMeasurementsColumnNames.points,
            ArrayType(
                StructType(
                    [
                        StructField(SilverMeasurementsColumnNames.Points.position, IntegerType(), True),
                        StructField(SilverMeasurementsColumnNames.Points.quantity, DecimalType(18, 3), True),
                        StructField(SilverMeasurementsColumnNames.Points.quality, StringType(), True),
                    ]
                ),
                True,
            ),
            True,
        ),
        StructField(SilverMeasurementsColumnNames.created, TimestampType(), True),
    ]
)
