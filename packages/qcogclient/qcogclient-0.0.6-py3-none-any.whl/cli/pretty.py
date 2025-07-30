import logging
import os
import traceback
from collections.abc import Callable, Coroutine
from typing import Any, Literal

import colorama

_OK_KEY = colorama.Fore.CYAN + colorama.Style.BRIGHT
_OK_VALUE = colorama.Fore.GREEN + colorama.Style.BRIGHT
_ERROR_KEY = colorama.Fore.RED + colorama.Style.BRIGHT
_ERROR_VALUE = colorama.Fore.RED + colorama.Style.BRIGHT
_WARNING_KEY = colorama.Fore.YELLOW + colorama.Style.BRIGHT
_WARNING_VALUE = colorama.Fore.YELLOW + colorama.Style.BRIGHT


def _display_response(response: Any) -> str:
    to_print = ""
    if isinstance(response, str):
        to_print = recurse(response, level="ok")
    elif isinstance(response, dict):
        if response.get("error") is not None:
            to_print = recurse(response["error"], level="error")
            to_print = f"❌  {to_print}"
        elif response.get("response") is not None:
            to_print = recurse(response["response"], level="ok")
            to_print = f"✅  {to_print}"
        elif response.get("warning") is not None:
            to_print = recurse(response["warning"], level="warning")
            to_print = f"⚠️  {to_print}"
        elif response.get("step") is not None:
            if len(response["step"]) != 1:
                raise ValueError(
                    f"Step must contain exactly one key. Got {response['step'].keys()}"
                )
            step_title = list(response["step"].keys())[0]
            to_print = recurse(response["step"][step_title], level="ok")
            to_print = f"🔄  {step_title}\n{to_print}"
    else:
        raise ValueError(f"Unknown response type: {type(response)}")
    return to_print


def display(logger: logging.Logger, async_: bool = False) -> Callable:
    def decorator(func: Callable) -> Callable | Coroutine:
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                response = func(*args, **kwargs)
                to_print = _display_response(response)
                logger.info(to_print)
                return response
            except Exception as e:
                to_print = _display_response({"error": str(e)})
                if os.environ.get("QCOG_DEBUG"):
                    stacktrace = traceback.format_exc()
                    to_print += f"\n{stacktrace}"
                logger.error(to_print)

        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                response = await func(*args, **kwargs)
                to_print = _display_response(response)
                logger.info(to_print)
                return response
            except Exception as e:
                to_print = _display_response({"error": str(e)})
                if os.environ.get("QCOG_DEBUG"):
                    stacktrace = traceback.format_exc()
                    to_print += f"\n{stacktrace}"
                logger.error(to_print)
                return None

        return async_wrapper if async_ else sync_wrapper

    return decorator


def KEY(key: str, level: Literal["ok", "error", "warning"] = "ok") -> str:
    return f"{_OK_KEY if level == 'ok' else _ERROR_KEY if level == 'error' else _WARNING_KEY}{key}{colorama.Style.RESET_ALL}:"  # noqa


def VALUE(value: Any, level: Literal["ok", "error", "warning"] = "ok") -> str:
    return f"{_OK_VALUE if level == 'ok' else _ERROR_VALUE if level == 'error' else _WARNING_VALUE}{value}{colorama.Style.RESET_ALL}"  # noqa


def SEPARATOR(indent: int = 0, length: int = 80, prefix: str = "") -> str:
    sep = f"\n{colorama.Style.BRIGHT}{colorama.Fore.BLUE}"
    sep += " " * indent
    sep += prefix
    sep += "=" * length
    sep += colorama.Style.RESET_ALL
    return sep


def recurse(
    value: Any, indent: int = 0, level: Literal["ok", "error", "warning"] = "ok"
) -> str:
    SPACE = " " * indent
    buffer = ""
    if isinstance(value, dict):
        buffer += "\n"
        for k, v in value.items():
            buffer += (
                f"{SPACE}{KEY(k, level=level)}{recurse(v, indent + 1, level=level)}\n"
            )
    elif isinstance(value, list):
        buffer += "\n"
        if len(value) == 0:
            return f"{SPACE}-{VALUE('No items', level=level)}\n"
        for i, v in enumerate(value):
            buffer += f"{SEPARATOR(indent=indent + 1, prefix=f'{i + 1}. ')}\n"
            buffer += f"{SPACE}{recurse(v, indent + 1, level=level)}\n"
    else:
        buffer += f"{SPACE}{VALUE(value, level=level)}"

    return buffer
