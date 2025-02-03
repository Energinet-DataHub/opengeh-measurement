import uuid

import pytest
from testcommon.container_test import DatabricksApiClient


def test__databricks_job_starts_and_stops_successfully(databricks_api_client: DatabricksApiClient) -> None:
    """
    Tests that a Databricks electrical heating job runs successfully to completion.
    """
    try:
        # Arrange
        job_id = databricks_api_client.get_job_id("ElectricalHeating")
        params = [
            f"--orchestration-instance-id={str(uuid.uuid4())}",
        ]

        # Act
        run_id = databricks_api_client.start_job(job_id, params)

        # Assert
        result = databricks_api_client.wait_for_job_completion(run_id)
        assert result.value == "SUCCESS", f"Job did not complete successfully: {result.value}"
    except Exception as e:
        pytest.fail(f"Databricks job test failed: {e}")
