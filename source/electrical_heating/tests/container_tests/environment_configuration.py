from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent.parent


class EnvironmentConfiguration(BaseSettings):
    """This class resides inside the container test folder because it is needed by the test framework.
    If placed outside the container test folder, it is not visible to the test framework when running
    i CD."""

    databricks_token: str = Field(alias="DATABRICKS_TOKEN")
    workspace_url: str = Field(alias="WORKSPACE_URL")

    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_ROOT}/tests/.env",
        env_file_encoding="utf-8",
    )
