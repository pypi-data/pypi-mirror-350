from abc import ABC
from os import getenv
from typing import Any, Optional

from .auth import AuthClient
from .const import SERVER_TPL, USER_AGENT


class BaseElevateClient(ABC):
    _route: str
    _conf_class: Any

    @property
    def auth(self) -> AuthClient:
        return self._auth

    @auth.setter
    def auth(self, auth_client: AuthClient) -> None:
        self._auth = auth_client

    def __init__(self, server: str, *args: Any, **kwargs: Any) -> None:
        base_url = SERVER_TPL.format(server) + self._route
        kwargs["configuration"] = self._conf_class(host=base_url)
        super().__init__(*args, **kwargs)
        self.user_agent = USER_AGENT


class BaseElevateService(ABC):
    _client_class: Any

    @staticmethod
    def _arg_env_err(value: Optional[str], env_key: str) -> str:
        if value:
            return value
        env_value = getenv(env_key)
        if env_value:
            return env_value
        raise LookupError(f"Missing {env_key}.")

    def __init__(
        self,
        server: Optional[str] = None,
        client_id: Optional[str] = None,
        secret_key: Optional[str] = None,
    ) -> None:
        """
        :param server: The base URL of the Elevate service API. If not provided, defaults to the `E2_SERVER` environment variable.
        :type server: str, optional
        :param client_id: The client ID for authentication. If not provided, defaults to the `E2_CLIENT_ID` environment variable.
        :type client_id: str, optional
        :param secret_key: The secret key for authentication. If not provided, defaults to the `E2_SECRET_KEY` environment variable.
        :type secret_key: str, optional
        """
        _server = self._arg_env_err(server, "E2_SERVER")
        _client_id = self._arg_env_err(client_id, "E2_CLIENT_ID")
        _secret_key = self._arg_env_err(secret_key, "E2_SECRET_KEY")

        self.api_client = self._client_class(_server)
        self.api_client.auth = AuthClient(self, _server, _client_id, _secret_key)
