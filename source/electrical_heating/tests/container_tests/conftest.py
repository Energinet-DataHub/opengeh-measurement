﻿import os
from pathlib import Path

import pytest
import yaml
from testcommon.container_test import DatabricksApiClient

PROJECT_ROOT = Path(__file__).parent.parent


def _load_settings_from_file(file_path: Path) -> dict:
    if file_path.exists():
        with file_path.open() as stream:
            return yaml.safe_load(stream)
    else:
        return {}


@pytest.fixture(scope="session")
def databricks_api_client() -> DatabricksApiClient:
    settings = _load_settings_from_file(PROJECT_ROOT / "tests" / "test.local.settings.yml")
    databricks_token = settings.get("DATABRICKS_TOKEN") or os.getenv("DATABRICKS_TOKEN")
    databricks_host = settings.get("WORKSPACE_URL") or os.getenv("WORKSPACE_URL")
    databricksApiClient = DatabricksApiClient(databricks_token, databricks_host)
    return databricksApiClient
