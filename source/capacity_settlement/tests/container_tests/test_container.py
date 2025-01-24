﻿import os
import time

import pytest
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import RunResultState


class DatabricksApiClient:

    def __init__(self) -> None:
        databricks_token = os.getenv('DATABRICKS_TOKEN')
        databricks_host = os.getenv('WORKSPACE_URL')
        
        self.client = WorkspaceClient(host=databricks_host, token=databricks_token)

    def start_job(self, job_id: int) -> int:
        """
        Starts a Databricks job using the Databricks SDK and returns the run ID.
        """
        response = self.client.jobs.run_now(job_id=job_id)
        return response.run_id

    def wait_for_job_completion(
        self, run_id: int, timeout: int = 300, poll_interval: int = 10
    ) -> RunResultState:
        """
        Waits for a Databricks job to complete.
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            run_status = self.client.jobs.get_run(run_id=run_id)
            if run_status.state is None:
                raise Exception("Job run status state is None")

            lifecycle_state = run_status.state.life_cycle_state
            result_state = run_status.state.result_state

            if lifecycle_state == "TERMINATED":
                if result_state is None:
                    raise Exception("Job terminated but result state is None")
                return result_state
            elif lifecycle_state == "INTERNAL_ERROR":
                raise Exception(
                    f"Job failed with an internal error: {run_status.state.state_message}"
                )

            time.sleep(poll_interval)

        raise TimeoutError(f"Job did not complete within {timeout} seconds.")


def test__databricks_job_starts_and_stops_successfully(  
) -> None:
    """
    Tests that a Databricks capacity settlement job runs successfully to completion.
    """
    try:
        # Arrange
        databricksApiClient = DatabricksApiClient()
        job_id = None
        job_list = databricksApiClient.client.jobs.list()
        for job in job_list:
            if job.settings is not None and job.settings.name == "CapacitySettlement":
                job_id = job.job_id
                break

        # Act
        if job_id is None:
            pytest.fail("Job ID for 'CapacitySettlement' not found.")
        run_id = databricksApiClient.start_job(job_id)

        # Assert
        result = databricksApiClient.wait_for_job_completion(run_id)
        assert result == "SUCCESS", f"Job did not complete successfully: {result}"
    except Exception as e:
        pytest.fail(f"Databricks job test failed: {e}")
