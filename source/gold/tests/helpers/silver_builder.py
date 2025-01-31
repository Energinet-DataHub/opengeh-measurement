import random
from datetime import datetime
from decimal import Decimal

from opengeh_gold.domain.schemas.silver_measurements import silver_measurements_schema


class SilverMeasurementsDataFrameBuilder:
    def __init__(self, spark_session):
        self.spark = spark_session
        self.data = []

    def add_row(
        self,
        orchestration_type="migrations",
        orchestration_instance_id="60a518a2-7c7e-4aec-8332",
        metering_point_id="503928175928475638",
        transaction_id="5a76d246-ceae-459f-9e9f",
        transaction_creation_datetime=None,
        metering_point_type="",
        product="",
        unit="",
        resolution="",
        start_datetime=None,
        end_datetime=None,
        points=None,
        created=None,
    ):
        if points is None:
            points = self._generate_default_points()
        self.data.append(
            (
                orchestration_type,
                orchestration_instance_id,
                metering_point_id,
                transaction_id,
                transaction_creation_datetime or datetime.now(),
                metering_point_type or random.choice(["E17", "E18", "E20", "D01", "D05", "D06", "D07", "D08"]),
                product,
                unit or random.choice(["KWH", "MWH", "MVARH", "KVARH", "KW"]),
                resolution or random.choice(["PT15M", "PT1H", "P1M"]),
                start_datetime or datetime.now(),
                end_datetime or datetime.now(),
                points,
                created or datetime.now(),
            )
        )
        return self

    def _generate_default_points(self):
        return [
            {
                "position": position,
                "quantity": Decimal(round(random.uniform(0, 1000), 3)),
                "quality": random.choice(["measured", "estimated", "calculated", "missing"]),
            }
            for position in range(1, 25)
        ]

    def build(self):
        return self.spark.createDataFrame(self.data, schema=silver_measurements_schema)
