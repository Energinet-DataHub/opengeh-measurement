import pyspark.sql.types as t

nullable = True


# Electrical heating calculations
calculations = t.StructType(
    [
        #
        # Calculation ID
        # The ID is generated by the calculation
        # UUID
        t.StructField("calculation_id", t.StringType(), not nullable),
        #
        # The ID of the orchestration instance that started the calculation
        t.StructField("orchestration_instance_id", t.StringType(), not nullable),
        #
        # The ID of the actor that created the orchestration instance
        # that started the calculation
        t.StructField("orchestration_instance_id", t.StringType(), not nullable),
        #
        # The time when the calculation was started (after cluster warm-up)
        # UTC time
        t.StructField(
            "execution_start_datetime",
            t.TimestampType(),
            not nullable,
        ),
        #
        # The time when the calculation terminated
        # UTC time
        t.StructField(
            "execution_stop_datetime",
            t.TimestampType(),
            not nullable,
        ),
    ]
)
