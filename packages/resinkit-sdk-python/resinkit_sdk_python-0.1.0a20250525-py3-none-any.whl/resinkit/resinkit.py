from typing import Optional

from flink_gateway_api import Client
from resinkit.core.task import Task
from resinkit.ui.tasks_management_ui import ResinkitAPIClient, TasksManagementUI
from resinkit.ui.variables_ui import VariablesUI


class Resinkit:
    def __init__(
        self,
        resinkit_session: Optional[str] = None,
        personal_access_token: Optional[str] = None,
        sql_gateway_url: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self._base_url = base_url
        self._sql_gateway_url = sql_gateway_url
        self._resinkit_session_id = resinkit_session
        self._personal_access_token = personal_access_token
        self._sql_gateway_client = Client(
            base_url=sql_gateway_url,
            raise_on_unexpected_status=True,
        )

        if resinkit_session:
            self._sql_gateway_client = self._sql_gateway_client.with_cookies(
                {"resink_session": resinkit_session}
            )

        if personal_access_token:
            self._sql_gateway_client = self._sql_gateway_client.with_headers(
                {"Authorization": personal_access_token}
            )

    def show_vars_ui(self, base_url: Optional[str] = None) -> None:
        """
        Display a UI for managing variables.

        Args:
            base_url: The base URL for the API. If not provided, uses the SQL gateway URL.

        Returns:
            A Panel UI component that can be displayed in a notebook.
        """
        api_url = base_url or self._base_url
        if not api_url:
            raise ValueError(
                "No API URL provided. Please provide a base_url or initialize Resinkit with sql_gateway_url."
            )

        ui = VariablesUI(
            base_url=api_url,
            session_id=self._resinkit_session_id,
            personal_access_token=self._personal_access_token,
        )
        return ui.show()

    def show_tasks_ui(self, base_url: Optional[str] = None) -> None:
        """
        Display a UI for managing tasks.

        Args:
            base_url: The base URL for the API. If not provided, uses the SQL gateway URL.

        Returns:
            A Panel UI component that can be displayed in a notebook.
        """
        api_url = base_url or self._base_url
        if not api_url:
            raise ValueError(
                "No API URL provided. Please provide a base_url or initialize Resinkit with sql_gateway_url."
            )

        api_client = ResinkitAPIClient(
            base_url=api_url,
            api_key=self._personal_access_token,
        )
        ui = TasksManagementUI(api_client=api_client)
        return ui.show()

    def get_task(self, task_id: str) -> Task:
        return Task(
            task_id=task_id,
            api_client=self._api_client,
        )
