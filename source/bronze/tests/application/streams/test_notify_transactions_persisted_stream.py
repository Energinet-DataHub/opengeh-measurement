# from unittest.mock import MagicMock, patch

# from opengeh_bronze.application.streams.notify_transactions_persisted_stream import (
#     notify,
#     notify_transactions_persisted,
# )
# from opengeh_bronze.domain.transformations.bronze_measurements_transformations import (
#     transform as bronze_measurements_transformations_transform,
# )
# from opengeh_bronze.domain.transformations.notify_transactions_persisted_events_transformation import (
#     transform as notify_transactions_persisted_events_transformation_transform,
# )
# from opengeh_bronze.infrastructure.streams.kafka_stream import KafkaStream


# def test__notify__calls_write_stream_with_bronze_stream_and_query_name_and_options_and_notify_transactions_persisted():
#     # Arrange
#     spark = MagicMock()
#     bronze_stream = MagicMock()
#     options = {"ignoreDeletes": "true"}
#     query_name = "query_name"
#     notify_transactions_persisted = MagicMock()

#     with (
#         patch(
#             "opengeh_bronze.application.streams.notify_transactions_persisted_stream.spark_session.initialize_spark",
#             return_value=spark,
#         ),
#         patch(
#             "opengeh_bronze.application.streams.notify_transactions_persisted_stream.BronzeRepository"
#         ) as BronzeRepository,
#         patch(
#             "opengeh_bronze.application.streams.notify_transactions_persisted_stream.writer.write_stream"
#         ) as writer_write_stream,
#         patch(
#             "opengeh_bronze.application.streams.notify_transactions_persisted_stream.notify_transactions_persisted"
#         ) as notify_transactions_persisted,
#     ):
#         # Act
#         notify()

#         # Assert
#         BronzeRepository.assert_called_once_with(spark)
#         BronzeRepository.return_value.read_submitted_transactions.assert_called_once_with()
#         writer_write_stream.assert_called_once_with(bronze_stream, query_name, options, notify_transactions_persisted)
#         notify_transactions_persisted.assert_not_called()
#         bronze_measurements_transformations_transform.assert_not_called()


# def test__notify_transactions_persisted__calls_transform_with_bronze_measurements_and_calls_transform_with_unpackaged_measurements_and_calls_transform_with_notify_transactions_persisted_events():
#     # Arrange

#     bronze_measurements = MagicMock()
#     batch_id = 1
#     unpackaged_measurements = MagicMock()
#     notify_transactions_persisted_events = MagicMock()

#     with (
#         patch(
#             "opengeh_bronze.application.streams.notify_transactions_persisted_stream.bronze_measurements_transformations.transform",
#             return_value=unpackaged_measurements,
#         ),
#         patch(
#             "opengeh_bronze.application.streams.notify_transactions_persisted_stream.notify_transactions_persisted_events_transformation.transform",
#             return_value=notify_transactions_persisted_events,
#         ),
#     ):
#         # Act
#         notify_transactions_persisted(bronze_measurements, batch_id)

#         # Assert
#         bronze_measurements_transformations_transform.assert_called_once_with(bronze_measurements)
#         notify_transactions_persisted_events_transformation_transform.assert_called_once_with(unpackaged_measurements)
#         KafkaStream().write_stream.assert_called_once_with(notify_transactions_persisted_events)
