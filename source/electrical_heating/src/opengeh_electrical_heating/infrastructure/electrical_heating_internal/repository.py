from pyspark.sql import SparkSession

from opengeh_electrical_heating.infrastructure.electrical_heating_internal.data_structure import Calculations


class Repository:
    def __init__(
        self,
        spark: SparkSession,
        catalog_name: str,
    ) -> None:
        self._spark = spark
        self._catalog_name = catalog_name

    def save(self, calculation: Calculations) -> None:
        # TODO Will implemented in another PR.
        pass
