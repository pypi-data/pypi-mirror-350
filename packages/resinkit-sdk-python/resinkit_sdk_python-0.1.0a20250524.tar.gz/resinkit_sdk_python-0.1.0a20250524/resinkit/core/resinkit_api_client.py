"""
ResInKit API Client for interacting with the ResInKit REST API.
"""

from typing import Optional, Dict, Any


class ResinkitAPIClient:
    """Client for interacting with the Resinkit API."""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the API client.

        Args:
            base_url: Base URL for the API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _get_headers(self) -> Dict[str, str]:
        """Get the headers for API requests."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def list_tasks(self, **kwargs) -> Dict[str, Any]:
        """List tasks with optional filtering."""
        import requests

        endpoint = f"{self.base_url}/api/v1/agent/tasks"
        response = requests.get(endpoint, headers=self._get_headers(), params=kwargs)
        response.raise_for_status()
        return response.json()

    def submit_task(self, task_config: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a new task with JSON configuration."""
        import requests

        endpoint = f"{self.base_url}/api/v1/agent/tasks"
        response = requests.post(
            endpoint, headers=self._get_headers(), json=task_config
        )
        response.raise_for_status()
        return response.json()

    def submit_yaml_task(self, yaml_config: str) -> Dict[str, Any]:
        """Submit a new task with YAML configuration."""
        import requests

        endpoint = f"{self.base_url}/api/v1/agent/tasks/yaml"
        headers = self._get_headers()
        headers["Content-Type"] = "text/plain"
        response = requests.post(endpoint, headers=headers, data=yaml_config)
        response.raise_for_status()
        return response.json()

    def get_task_details(self, task_id: str) -> Dict[str, Any]:
        """Get details of a specific task."""
        import requests

        endpoint = f"{self.base_url}/api/v1/agent/tasks/{task_id}"
        response = requests.get(endpoint, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def cancel_task(
        self, task_id: str, reason: Optional[str] = None, force: bool = False
    ) -> Dict[str, Any]:
        """Cancel a task."""
        import requests

        endpoint = f"{self.base_url}/api/v1/agent/tasks/{task_id}/cancel"
        payload = {"reason": reason, "force": force}
        response = requests.post(endpoint, headers=self._get_headers(), json=payload)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def get_task_logs(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Get logs for a specific task."""
        import requests

        endpoint = f"{self.base_url}/api/v1/agent/tasks/{task_id}/logs"
        response = requests.get(endpoint, headers=self._get_headers(), params=kwargs)
        response.raise_for_status()
        return response.json()

    def get_task_results(self, task_id: str) -> Dict[str, Any]:
        """Get results of a completed task."""
        import requests

        endpoint = f"{self.base_url}/api/v1/agent/tasks/{task_id}/results"
        response = requests.get(endpoint, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def permanently_delete_task(self, task_id: str) -> Dict[str, Any]:
        """Permanently delete a task and its events if the task is in an end state."""
        import requests

        endpoint = f"{self.base_url}/api/v1/agent/tasks/{task_id}/permanent"
        response = requests.delete(endpoint, headers=self._get_headers())
        if response.status_code == 204:
            return {"message": "Task deleted permanently."}
        else:
            try:
                return response.json()
            except Exception:
                response.raise_for_status()
