import opengeh_bronze.application.config.spark_session as spark_session
from opengeh_bronze.infrastructure.streams.kafka_stream import KafkaStream


def submit_transactions() -> None:
    spark = spark_session.initialize_spark()
    KafkaStream().submit_transactions(spark)
