import pandas as pd
from typing import Optional, Union, List, Dict, Any
from resinkit.core.resinkit_api_client import ResinkitAPIClient


class Task:
    """
    A class for interacting with ResInKit tasks and retrieving results as pandas DataFrames.

    Usage:
        task = Task("flink_sql_NtPBUmwDr", base_url="http://localhost:8080")
        df = task.result_df()
    """
    __slots__ = ("task_id")

    def __init__(
        self,
        task_id: str,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize a Task instance.

        Args:
            task_id: The unique identifier for the task
            base_url: Base URL for the API (e.g., "http://localhost:8080")
            api_key: Optional API key for authentication
        """
        self.task_id = task_id
        self.api_client = ResinkitAPIClient(base_url=base_url, api_key=api_key)
        self._task_details = None
        self._task_results = None

    def get_task_info(self) -> Dict[str, Any]:
        """
        Get detailed information about the task.

        Returns:
            Dict containing task details including status, created_at, submitted_configs, etc.
        """
        if self._task_details is None:
            self._task_details = self.api_client.get_task_details(self.task_id)
        return self._task_details

    def get_task_results(self) -> Dict[str, Any]:
        """
        Get the raw results of the task.

        Returns:
            Dict containing task results including result_summary, results, job_ids, is_query flags, etc.
        """
        if self._task_results is None:
            self._task_results = self.api_client.get_task_results(self.task_id)
        return self._task_results

    def get_result_df(self) -> List[pd.DataFrame]:
        """
        Get query results as pandas DataFrame(s).

        For multiple SQL statements, only returns results where "is_query" is True.

        Returns:
            - If there's only one query result: pandas DataFrame
            - If there are multiple query results: List[pandas.DataFrame]

        Raises:
            ValueError: If no query results are found or task failed
            RuntimeError: If task is not completed
        """
        # Get task info to check status
        task_info = self.get_task_info()

        if task_info.get("status") != "COMPLETED":
            raise RuntimeError(
                f"Task {self.task_id} is not completed. Current status: {task_info.get('status')}"
            )

        if task_info.get("error_info"):
            error_info = task_info["error_info"]
            error_msg = error_info.get("message", "Unknown error")
            raise ValueError(f"Task {self.task_id} failed with error: {error_msg}")

        # Get task results
        results = self.get_task_results()

        # Extract result_summary
        result_data = results.get("data", {})
        if not result_data:
            raise ValueError(f"No result data found for task {self.task_id}")

        # Get the results array, is_query flags, and results data
        results_list = result_data.get("results", [])
        is_query_list = result_data.get("is_query", [])

        if not results_list or not is_query_list:
            raise ValueError(
                f"No results or is_query information found for task {self.task_id}"
            )

        if len(results_list) != len(is_query_list):
            raise ValueError(
                f"Mismatch between results and is_query arrays for task {self.task_id}"
            )

        # Filter for query results only
        query_results = []
        for i, (result, is_query) in enumerate(zip(results_list, is_query_list)):
            if is_query and isinstance(result, list) and len(result) > 0:
                # Convert result to DataFrame
                df = pd.DataFrame(result)
                query_results.append(df)

        if not query_results:
            raise ValueError(
                f"No query results found for task {self.task_id}. All statements were non-query operations."
            )

        return query_results

    @property
    def status(self) -> str:
        """Get the current status of the task."""
        return self.get_task_info().get("status", "UNKNOWN")

    @property
    def task_type(self) -> str:
        """Get the type of the task."""
        return self.get_task_info().get("task_type", "UNKNOWN")

    @property
    def created_at(self) -> str:
        """Get the creation timestamp of the task."""
        return self.get_task_info().get("created_at", "")

    @property
    def finished_at(self) -> str:
        """Get the finish timestamp of the task."""
        return self.get_task_info().get("finished_at", "")

    def __repr__(self) -> str:
        return f"Task(task_id='{self.task_id}', status='{self.status}', task_type='{self.task_type}')"
