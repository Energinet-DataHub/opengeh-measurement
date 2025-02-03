from pydantic_settings import SettingsConfigDict

from opengeh_capacity_settlement.application.job_args.capacity_settlement_args import CapacitySettlementArgs


class CapacitySettlementTestArgs(CapacitySettlementArgs):
    """Args for testing the electrical heating job."""

    def __init__(self, env_file_path: str) -> None:
        """Inherits from CapacitySettlementArgs, but overrides constructor by pointing to a specific path for environment files"""
        self.__class__.model_config = SettingsConfigDict(env_file=env_file_path, populate_by_name=True)
        super().__init__()
