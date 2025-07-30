import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any
from ..core.resinkit_api_client import ResinkitAPIClient


class VariablesUI:
    def __init__(
        self,
        base_url: str,
        session_id: Optional[str] = None,
        personal_access_token: Optional[str] = None,
    ):
        self.base_url = base_url
        self.session_id = session_id
        self.personal_access_token = personal_access_token
        self.variables = []

        # Initialize API client
        self.api_client = ResinkitAPIClient(
            base_url=base_url, api_key=personal_access_token, session_id=session_id
        )

        # Initialize Panel components
        pn.extension()

        # Create main UI components
        self.variables_table = pn.widgets.Tabulator(
            height=400, layout="fit_columns", sizing_mode="stretch_width"
        )

        # Configure table columns
        self.variables_table.formatters = {"actions": {"type": "html"}}
        self.variables_table.widths = {"actions": 120}
        self.variables_table.titles = {
            "name": "Name",
            "description": "Description",
            "actions": "Actions",
        }

        # Updated buttons with icons
        self.add_button = pn.widgets.Button(
            name="+ Add Variable", button_type="primary", width=150
        )
        self.refresh_button = pn.widgets.Button(
            name="↻ Refresh", button_type="default", width=100
        )

        # Form components
        self.name_input = pn.widgets.TextInput(
            name="Name", placeholder="Enter variable name"
        )
        self.value_input = pn.widgets.TextInput(
            name="Value", placeholder="Enter variable value"
        )
        self.description_input = pn.widgets.TextAreaInput(
            name="Description", placeholder="Enter description", max_length=500, rows=3
        )
        self.submit_button = pn.widgets.Button(name="Submit", button_type="primary")
        self.cancel_button = pn.widgets.Button(name="Cancel", button_type="default")

        # Variable value view components
        self.var_name_display = pn.widgets.StaticText(name="Name")
        self.var_value_display = pn.widgets.TextAreaInput(
            name="Value", disabled=True, rows=3
        )
        self.var_description_display = pn.widgets.StaticText(name="Description")
        self.back_button = pn.widgets.Button(name="Back", button_type="default")
        self.back_button.on_click(self._show_variables_table)

        # Set up callbacks
        self.add_button.on_click(self._show_add_form)
        self.refresh_button.on_click(self._refresh_variables)
        self.submit_button.on_click(self._submit_variable)
        self.cancel_button.on_click(self._show_variables_table)

        # Status notification
        self.notification = pn.widgets.StaticText(value="", styles={"color": "red"})

        # Updated layout with buttons on the right
        self.table_view = pn.Column(
            pn.Row(
                pn.pane.Markdown("# Variables", sizing_mode="stretch_width"),
                pn.Row(self.refresh_button, self.add_button, sizing_mode="fixed"),
                sizing_mode="stretch_width",
            ),
            self.notification,
            self.variables_table,
        )

        self.form_view = pn.Column(
            pn.pane.Markdown("# Add Variable"),
            self.name_input,
            self.value_input,
            self.description_input,
            self.notification,
            pn.Row(self.submit_button, self.cancel_button),
        )

        self.value_view = pn.Column(
            pn.pane.Markdown("# Variable Details"),
            self.var_name_display,
            self.var_value_display,
            self.var_description_display,
            pn.Row(self.back_button),
        )

        self.main = pn.Column(self.table_view)

    def _load_variables(self) -> List[Dict[str, Any]]:
        """Fetch variables from API"""
        try:
            variables = self.api_client.list_variables()

            # Add action buttons to each row
            for var in variables:
                var["actions"] = (
                    f'<button class="btn btn-danger btn-sm delete-btn" data-var-name="{var["name"]}">Delete</button>'
                )

            return variables
        except Exception as e:
            self.notification.value = f"Error loading variables: {e}"
            return []

    def _get_variable(self, name: str) -> Dict[str, Any]:
        """Get a specific variable including its value"""
        try:
            return self.api_client.get_variable(name)
        except Exception as e:
            self.notification.value = f"Error fetching variable {name}: {e}"
            return {}

    def _refresh_variables(self, event=None):
        """Refresh the variables table"""
        self.notification.value = ""
        self.variables = self._load_variables()

        # Convert list of dictionaries to pandas DataFrame
        if self.variables:
            self.variables_table.value = pd.DataFrame(self.variables)
        else:
            self.variables_table.value = pd.DataFrame(
                columns=["name", "description", "actions"]
            )

        # Create JS callback for button clicks
        self.variables_table.on_click(self._table_action_callback)

    def _table_action_callback(self, event):
        """Handle table row action button clicks"""
        if event.column == "actions" and event.value:
            # Check if DataFrame has data and row index is valid
            if (
                self.variables_table.value is not None
                and len(self.variables_table.value) > 0
            ):
                try:
                    # Get variable name from the DataFrame
                    var_name = self.variables_table.value.iloc[event.row]["name"]

                    if "delete-btn" in event.value:
                        self._delete_variable(var_name)
                except IndexError:
                    self.notification.value = f"Error: Could not access row {event.row}. Please refresh the table."
                except Exception as e:
                    self.notification.value = f"Error processing action: {e}"

    def _show_variable_details(self, name: str):
        """Show variable details including the value"""
        var_details = self._get_variable(name)

        if var_details:
            self.var_name_display.value = var_details.get("name", "")
            self.var_value_display.value = var_details.get("value", "")
            self.var_description_display.value = var_details.get("description", "")

            self.main.clear()
            self.main.append(self.value_view)

    def _delete_variable(self, name: str):
        """Delete a variable"""
        try:
            self.api_client.delete_variable(name)
            self.notification.value = f"Variable '{name}' deleted successfully"
            self._refresh_variables()
        except Exception as e:
            self.notification.value = f"Error deleting variable {name}: {e}"

    def _show_add_form(self, event=None):
        """Show the add variable form"""
        self.notification.value = ""
        self.name_input.value = ""
        self.value_input.value = ""
        self.description_input.value = ""
        self.main.clear()
        self.main.append(self.form_view)

    def _show_variables_table(self, event=None):
        """Show the variables table"""
        self.notification.value = ""
        self.main.clear()
        self.main.append(self.table_view)
        self._refresh_variables()

    def _submit_variable(self, event=None):
        """Submit a new variable"""
        name = self.name_input.value
        value = self.value_input.value
        description = self.description_input.value

        if not name or not value:
            self.notification.value = "Name and value are required"
            return

        try:
            self.api_client.create_variable(name, value, description)

            # Clear form and return to table view
            self.notification.value = f"Variable '{name}' created successfully"
            self._show_variables_table()
        except Exception as e:
            self.notification.value = f"Error adding variable: {e}"

    def show(self):
        """Display the UI"""
        self._refresh_variables()
        return self.main
