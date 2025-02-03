import os
import uuid
from typing import Tuple, Type

from pydantic import Field
from pydantic_settings import BaseSettings, CliSettingsSource, PydanticBaseSettingsSource, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class CapacitySettlementArgs(BaseSettings):
    """Base settings to contain run parameters for the job."""

    orchestration_instance_id: uuid.UUID = Field(..., alias="orchestration-instance-id")
    time_zone: str = "Europe/Copenhagen"
    calculation_month: int = Field(..., alias="calculation-month")
    calculation_year: int = Field(..., alias="calculation-year")
    model_config = SettingsConfigDict(
        env_file=DOTENV,
        populate_by_name=True,  # Allow access using both alias and field name
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            CliSettingsSource(settings_cls, cli_parse_args=True, cli_ignore_unknown_args=True),
            env_settings,
            dotenv_settings,
        )
