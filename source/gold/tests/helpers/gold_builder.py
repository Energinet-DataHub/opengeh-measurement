import random
from datetime import datetime
from decimal import Decimal

from opengeh_gold.domain.schemas.gold_measurements import gold_measurements_schema


class GoldMeasurementsDataFrameBuilder:
    def __init__(self, spark_session):
        self.spark = spark_session
        self.data = []

    def add_row(
        self,
        metering_point_id="502938475674839281",
        observation_time=None,
        quantity=Decimal("0.000"),
        quality=None,
        metering_point_type="",
        transaction_id="",
        transaction_creation_datetime=None,
        created=None,
        modified=None,
    ):
        self.data.append(
            (
                metering_point_id,
                observation_time or datetime.now(),
                quantity or Decimal(round(random.uniform(0, 1000), 3)),
                quality or random.choice(["measured", "estimated", "calculated", "missing"]),
                metering_point_type or random.choice(["E17", "E18", "E20", "D01", "D05", "D06", "D07", "D08"]),
                transaction_id,
                transaction_creation_datetime or datetime.now(),
                created or datetime.now(),
                modified or datetime.now(),
            )
        )
        return self

    def build(self):
        return self.spark.createDataFrame(self.data, schema=gold_measurements_schema)
