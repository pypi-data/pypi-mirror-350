from __future__ import annotations

from functools import wraps
from http import HTTPStatus
from inspect import getmembers, ismethod
from typing import Any, Callable, Protocol

import jwt
import urllib3

from .const import SERVER_TPL


class AccessDeniedException(Exception):
    pass


class AuthHeaderInjectable(Protocol):
    def set_default_header(self, header_name: str, header_value: str) -> None: ...
    @property
    def auth(self) -> AuthClient: ...


class AuthHeaderInjectableHolder(Protocol):
    @property
    def api_client(self) -> AuthHeaderInjectable: ...


class AuthClient:
    _http_client = urllib3.PoolManager()
    _exchange_route = "/exchange-auth-code"
    _exchange_method = "POST"
    _exchange_resp_key = "accessToken"
    _decode_opts = {"verify_signature": False, "verify_exp": True}

    def __init__(
        self,
        holder: AuthHeaderInjectableHolder,
        server: str,
        client_id: str,
        secret_key: str,
    ) -> None:
        self._url = SERVER_TPL.format(server) + AuthClient._exchange_route
        self._client_id = client_id
        self._secret_key = secret_key

        self._set_new_token()
        AuthClient.register_auth_header_injector(holder)

    @property
    def _api_credentials_payload(self) -> dict:
        return {"clientId": self._client_id, "secret": self._secret_key}

    @property
    def header(self) -> dict:
        self._decode_jwt_with_regenerate()
        return {"header_name": "Authorization", "header_value": f"Bearer {self._token}"}

    def _jwt_decode(self) -> None:
        jwt.decode(self._token, options=AuthClient._decode_opts)

    def _decode_jwt_with_regenerate(self) -> None:
        try:
            self._jwt_decode()
        except jwt.exceptions.ExpiredSignatureError:
            self._set_new_token()
            self._jwt_decode()

    def _set_new_token(self) -> None:
        resp = AuthClient._http_client.request(
            method=AuthClient._exchange_method,
            json=self._api_credentials_payload,
            url=self._url,
        )
        if resp.status != HTTPStatus.OK:
            raise AccessDeniedException("Invalid credentials.")
        self._token = resp.json()[AuthClient._exchange_resp_key]

    @staticmethod
    def auth_header_injector(
        holder: AuthHeaderInjectableHolder, func: Callable
    ) -> Callable:
        @wraps(func)
        def injected_method(*args: Any, **kwargs: Any) -> Any:
            holder.api_client.set_default_header(**holder.api_client.auth.header)
            result = func(*args, **kwargs)
            return result

        return injected_method

    @classmethod
    def register_auth_header_injector(cls, holder: AuthHeaderInjectableHolder) -> None:
        for func in getmembers(holder, ismethod):
            func_name, original_func = func[0], func[1]
            if not func_name.startswith("_"):
                decorated_func = cls.auth_header_injector(holder, original_func)
                setattr(holder, func_name, decorated_func)
