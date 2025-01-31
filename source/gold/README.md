# Gold Layer

This python package handles streaming from the silver layer, to the gold layer.

## Gold Schema

See the [gold measurements](src/opengeh_gold/domain/schemas/gold_measurements.py) schema for more information, on the columns and data types used in the gold layer.

## Gold Transformations

The transformation from the Silver layer to the Gold layer consists of the following steps:

- **Exploding silver `points` column**: Each point in the `points` array is expanded into its own row, flattening the data.
- **Transforming `observation_time`**: The observation time is derived based on the resolution of the measurement:
    - **Monthly resolution (`P1M`)**: If the `start_datetime` is the first day of the month, months are added based on the point’s position value. Otherwise, if the position is the first one, `start_datetime` is kept; otherwise, the month is  truncated, and months are added according to the position value.
    - **Hourly resolution (`PT1H`)**: The `observation_time` is calculated by adding `(position - 1) * 1 hour` to `start_datetime`.
    - **15-minute resolution (`PT15M`)**: The `observation_time` is calculated by adding `(position - 1) * 15 minutes` to `start_datetime`.
    - **Fallback**: If none of these conditions are met, `start_datetime` is used as the `observation_time`.
