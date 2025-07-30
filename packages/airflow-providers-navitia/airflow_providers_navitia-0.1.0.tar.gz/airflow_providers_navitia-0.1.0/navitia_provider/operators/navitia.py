from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from navitia_client.client.exceptions import NavitiaAccessTokenMissingError, NavitiaForbiddenAccessError

from navitia_provider.hooks.navitia import NavitiaHook

if TYPE_CHECKING:
    from airflow.utils.context import Context


class NavitiaOperator(BaseOperator):
    """
    Interact and perform actions on Navitia API.

    This operator is designed to use Navitia Python Client: https://github.com/jonperron/python-navitia-client

    :param navitia_conn_id: Reference to a pre-defined Navitia Connection
    :param navitia_method: Method name from Navitia Client to be called
    :param navitia_method_args: Method parameters for the navitia_method
    :param result_processor: Function to further process the response from the Navitia API
    """

    def __init__(
        self,
        *,
        navitia_method: str,
        navitia_conn_id: str = "navitia_default",
        navitia_method_args: dict | None = None,
        result_processor: Callable | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.navitia_conn_id = navitia_conn_id
        self.method_name = navitia_method
        self.navitia_method_args = navitia_method_args or {}
        self.result_processor = result_processor

    def execute(self, context: Context) -> Any:
        try:
            hook = NavitiaHook(navitia_conn_id=self.navitia_conn_id)
            resource = hook.client

            result = getattr(resource, self.method_name)(
                **self.navitia_method_args
            )
            if self.result_processor:
                return self.result_processor(result)

            return result

        except (NavitiaAccessTokenMissingError, NavitiaForbiddenAccessError) as navitia_error:
            raise AirflowException(
                f"Failed to execute NavitiaOperator, error: {navitia_error}"
            )
        except Exception as exc:
            raise AirflowException(f"NavitiaOperator error: {exc}")
