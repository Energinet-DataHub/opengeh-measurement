from dataclasses import dataclass

from pyspark.sql import DataFrame

from opengeh_electrical_heating.domain.calculation import CalculatedMeasurementsDaily


@dataclass
class CalculationOutput:
    """Contains the output of a calculation."""

    measurements: CalculatedMeasurementsDaily

    calculations: DataFrame
