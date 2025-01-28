import opengeh_bronze.application.streams.notify_transactions_persisted_stream as notify_transactions_persisted_stream
import opengeh_bronze.migrations.migrations_runner as migrations_runner


def migrate() -> None:
    migrations_runner.migrate()


def notify_transactions_persisted() -> None:
    notify_transactions_persisted_stream.notify()
