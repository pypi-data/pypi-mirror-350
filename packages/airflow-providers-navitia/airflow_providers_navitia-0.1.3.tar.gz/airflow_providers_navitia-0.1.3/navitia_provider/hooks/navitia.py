"""This module allows to connect to Navitia."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from navitia_client.client import NavitiaClient


class NavitiaHook(BaseHook):
    """
    Interact with Navitia.

    Performs a connection to Navitia and retrieves client.

    :param navitia_conn_id: Reference to :ref:`Navitia connection id <howto/connection: navitia>`.
    """

    conn_name_attr = "navitia_conn_id"
    default_conn_name = "navitia_default"
    conn_type = "navitia"
    hook_name = "navitia"

    def __init__(
        self, navitia_conn_id: str = default_conn_name, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.navitia_conn_id = navitia_conn_id
        self.client: NavitiaClient | None = None
        self.get_conn()

    def get_conn(self) -> NavitiaClient:
        """Initiate a new connection with API key"""
        if self.client is not None:
            return self.client

        conn = self.get_connection(self.navitia_conn_id)
        api_key = conn.password

        if not api_key:
            raise AirflowException("An API Key is mandatory to access Navitia")

        self.client = NavitiaClient(auth=api_key)

        return self.client

    def test_connection(self) -> tuple[bool, str]:
        """Test connection"""
        conn = self.get_connection(self.navitia_conn_id)

        try:
            if TYPE_CHECKING:
                assert self.client
            self.client
            return True, "Successfully connected to Navitia."
        except Exception as exc:
            return False, str(exc)

    @staticmethod
    def get_ui_field_behaviour() -> dict[str, Any]:
        """Returns custom field behaviour"""

        return {
            "hidden_fields": ["schema", "login", "port", "extra"],
            "relabeling": {
                "password": "Navitia API key",
            },
        }
