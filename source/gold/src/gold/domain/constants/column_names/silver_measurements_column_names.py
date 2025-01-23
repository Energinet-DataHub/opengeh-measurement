﻿# TODO: Should reference Silver Package, figure out how to using git refs in uv
class SilverMeasurementsColumnNames:
    orchestration_type = "orchestration_type"
    orchestration_instance_id = "orchestration_instance_id"
    metering_point_id = "metering_point_id"
    transaction_id = "transaction_id"
    transaction_creation_datetime = "transaction_creation_datetime"
    metering_point_type = "metering_point_type"
    product = "product"
    unit = "unit"
    resolution = "resolution"
    start_datetime = "start_datetime"
    end_datetime = "end_datetime"
    points = "points"
    created = "created"

    class Points:
        """Constants for the column names in the points column of the silver measurements table.
        """
        position = "position"
        quantity = "quantity"
        quality = "quality"
