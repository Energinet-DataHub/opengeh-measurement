﻿import time

import pytest
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import RunResultState


class DatabricksApiClient:

    def __init__(self, host: str | None, token: str | None):
        self.client = WorkspaceClient(host=host, token=token)

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
    databricks_client: DatabricksApiClient,
) -> None:
    """
    Tests that a Databricks capacity settlement job runs successfully to completion.
    """
    try:
        # TODO AJW Arrange - Change job id to an capacity settlement job id - currently it's an electrical heating job id
        job_id = 195320213583647

        # Act
        run_id = databricks_client.start_job(job_id)

        # Assert
        result = databricks_client.wait_for_job_completion(run_id)
        assert result == "SUCCESS", f"Job did not complete successfully: {result}"
    except Exception as e:
        pytest.fail(f"Databricks job test failed: {e}")
