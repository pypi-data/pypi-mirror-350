from __future__ import annotations

import os
from typing import Any

import aiohttp
from pydantic import Field
from pydantic_settings import BaseSettings
import io

DEFAULT_ENV = "DEV"


def get_base_url() -> str:
    env = os.getenv("QCOG_ENV", DEFAULT_ENV)
    if env == "DEV":
        return "http://localhost:8001/api"
    elif env == "STAGING":
        return "http://qcog-api-staging-lb-690850646.us-east-2.elb.amazonaws.com/api"
    elif env == "PROD":
        return "https://qcog-api.qcog.ai/api"
    elif env == "TEST":
        return "http://testserver:50000/api"  # Starlette host enabled test client
    else:
        raise ValueError(f"Invalid environment: {env}")


DEFAULT_BASE_URL = get_base_url()

SSL = False


class HttpClientConfig(BaseSettings):
    api_key: str | None = Field(default=None, alias="QCOG_API_KEY")
    basic_auth_username: str | None = Field(
        default=None, alias="QCOG_BASIC_AUTH_USERNAME"
    )
    basic_auth_password: str | None = Field(
        default=None, alias="QCOG_BASIC_AUTH_PASSWORD"
    )
    model_config = {
        "env_file": ".env",
        "extra": "allow",
    }


class HttpClient:
    base_url: str
    api_version: str
    api_key: str | None
    basic_auth_username: str | None
    basic_auth_password: str | None

    @classmethod
    def with_api_key(cls, api_key: str) -> HttpClient:
        return cls._init(api_key=api_key)

    @classmethod
    def with_basic_auth(
        cls,
        username: str,
        password: str,
    ) -> HttpClient:
        return cls._init(
            basic_auth_username=username,
            basic_auth_password=password,
        )

    @classmethod
    def _init(
        cls,
        *,
        base_url: str = DEFAULT_BASE_URL,
        api_version: str = "v1",
        api_key: str | None = None,
        basic_auth_username: str | None = None,
        basic_auth_password: str | None = None,
    ) -> HttpClient:
        self = cls()
        self.base_url = base_url
        self.api_version = api_version
        self.api_key = api_key
        self.basic_auth_username = basic_auth_username
        self.basic_auth_password = basic_auth_password
        return self

    @property
    def url(self) -> str:
        return f"{self.base_url}/{self.api_version}/"

    def set_auth(self) -> aiohttp.BasicAuth | None:
        return (
            aiohttp.BasicAuth(
                self.basic_auth_username,
                self.basic_auth_password,
            )
            if (
                hasattr(self, "basic_auth_username")
                and hasattr(self, "basic_auth_password")
                and self.basic_auth_username
                and self.basic_auth_password
            )
            else None
        )

    def set_headers(self) -> dict[str, Any] | None:
        return (
            {
                "Authorization": f"x-api-key {self.api_key}" if self.api_key else None,  # noqa: E501
            }
            if hasattr(self, "api_key") and self.api_key
            else None
        )


    async def parse_client_response(self, response: aiohttp.ClientResponse) -> dict[str, Any]:
        data_response = await response.json()
        if "detail" in data_response:
            return {
                "error": data_response["detail"],
            }
        return {
            "response": data_response,
        }

    async def exec(
        self,
        url: str,
        method: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        auth = self.set_auth()
        headers = self.set_headers()

        try:
            async with aiohttp.ClientSession(
                auth=auth if not headers else None,
                headers=headers,  # type: ignore
            ) as session:
                if url.startswith("/"):
                    url = url[1:]

                full_url = f"{self.url}{url}"

                async with session.request(
                    method,
                    full_url,
                    json=data,
                    params=params,
                    # ssl=SSL,
                ) as response:
                    return await self.parse_client_response(response)

        except Exception as e:
            raise e

    async def upload_file(
        self,
        url: str,
        readable_stream: io.BytesIO,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        if url.startswith("/"):
            url = url[1:]

        full_url = f"{self.url}{url}"

        auth = self.set_auth()
        headers = self.set_headers()

        async with aiohttp.ClientSession(
            auth=auth if not headers else None,
            headers=headers,  # type: ignore
        ) as session:
            async with session.post(
                full_url,
                data={"file": readable_stream},
                params=params,
            ) as response:
                return await self.parse_client_response(response)


def init_client(
    api_key: str | None = None,
    basic_auth_username: str | None = None,
    basic_auth_password: str | None = None,
) -> HttpClient:
    """Initialize a client with the given api key and basic auth credentials.

    If no api key or basic auth credentials are provided, the client will try to get
    an api key from the store.

    The order of precedence is:
    1. api key provided as an argument
    2. api key in configuration (`.env` or `QCCOG_API_KEY`)
    """
    config = HttpClientConfig()
    client: HttpClient | None = None

    if (basic_auth_username or config.basic_auth_username) and (
        basic_auth_password or config.basic_auth_password
    ):
        basic_auth_username = basic_auth_username or config.basic_auth_username
        basic_auth_password = basic_auth_password or config.basic_auth_password
        assert basic_auth_username
        assert basic_auth_password
        client = HttpClient.with_basic_auth(
            basic_auth_username,
            basic_auth_password,
        )
    elif api_key or config.api_key:
        api_key = api_key or config.api_key
        assert api_key
        client = HttpClient.with_api_key(api_key)
    else:
        raise ValueError("No API key or basic auth credentials provided")

    return client
