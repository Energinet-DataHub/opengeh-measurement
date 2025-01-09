﻿import time

import pytest
from databricks.sdk import WorkspaceClient

JOB_ID = 576172778546244


class DataBricksClient:

    # constructor
    def __init__(self):
        self.client = WorkspaceClient(host=self.host)

    def start_job(self, job_id: int) -> int:
        """
        Starts a Databricks job using the Databricks SDK and returns the run ID.
        """
        response = self.client.jobs.run_now(job_id=job_id)
        return response.run_id

    @staticmethod
    def wait_for_job_completion(self, run_id: int, timeout=300, poll_interval=10):
        """
        Waits for a Databricks job to complete.
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            run_status = self.client.jobs.get_run(run_id=run_id)
            lifecycle_state = run_status.state.life_cycle_state
            result_state = run_status.state.result_state

            print(f"Job status: {lifecycle_state}, result: {result_state}")

            if lifecycle_state == "TERMINATED":
                return result_state
            elif lifecycle_state == "INTERNAL_ERROR":
                raise Exception(
                    f"Job failed with an internal error: {run_status.state.state_message}"
                )

            time.sleep(poll_interval)

        raise TimeoutError(f"Job did not complete within {timeout} seconds.")


@pytest.mark.parametrize("job_id", [JOB_ID])
def test__databricks_job_starts_and_stops_successfully(job_id):
    """
    Tests that a Databricks job runs successfully to completion.
    """
    try:
        # Arrange
        client = DataBricksClient()

        # Act
        run_id = client.start_job(job_id)

        # Assert
        result = client.wait_for_job_completion(client, run_id)
        assert result == "SUCCESS", f"Job did not complete successfully: {result}"
    except Exception as e:
        pytest.fail(f"Databricks job test failed: {e}")
