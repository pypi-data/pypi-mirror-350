from typing import Literal, Protocol, TypeVar


class HttpClientProtocol(Protocol):
    basic_auth_username: str | None
    basic_auth_password: str | None
    api_key: str | None


class WithClientProtocol(Protocol):
    client: HttpClientProtocol


def _validate(
    client: WithClientProtocol,
    auth_type: Literal["basic", "api_key"],
) -> None:
    if auth_type == "basic":
        if not client.client.basic_auth_username:
            raise ValueError("Basic Auth username is not set")
        if not client.client.basic_auth_password:
            raise ValueError("Basic Auth password is not set")
    elif auth_type == "api_key":
        if not client.client.api_key:
            raise ValueError("API key is not set")


T = TypeVar("T")
