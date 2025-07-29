"""Utility functions for Reflex Enterprise."""

import inspect
from typing import Any, Callable

from reflex import constants
from reflex.config import get_config
from reflex.utils import console, prerequisites
from reflex.vars.base import Var, VarData
from reflex.vars.function import ArgsFunctionOperation, FunctionStringVar

from .vars import ArgsFunctionOperationPromise, PromiseVar


def check_config_option_in_tier(
    option_name: str,
    allowed_tiers: list[str],
    fallback_value: Any,
    help_link: str | None = None,
):
    """Check if a config option is allowed for the authenticated user's current tier.

    Args:
        option_name: The name of the option to check.
        allowed_tiers: The tiers that are allowed to use the option.
        fallback_value: The fallback value if the option is not allowed.
        help_link: The help link to show to a user that is authenticated.
    """
    config = get_config()
    current_tier = prerequisites.get_user_tier()

    if allowed_tiers == []:
        the_remedy = "This option is not available in the current context."
    else:
        if current_tier == "anonymous":
            the_remedy = "You are currently logged out. Run `reflex login` to access this option."
        else:
            the_remedy = (
                f"Your current subscription tier is `{current_tier}`. "
                f"Please upgrade to {allowed_tiers} to access this option. "
            )
            if help_link:
                the_remedy += f"See {help_link} for more information."

    value = getattr(config, option_name)

    if value is None:
        setattr(config, option_name, fallback_value)
        return

    if value != fallback_value and current_tier not in allowed_tiers:
        console.warn(f"Config option `{option_name}` is restricted. {the_remedy}")
        setattr(config, option_name, fallback_value)
        config._set_persistent(**{option_name: fallback_value})


def is_deploy_context():
    """Check if the current context is a deploy context.

    Returns:
        True if the current context is a deploy context, False otherwise.
    """
    from reflex.utils.exec import get_compile_context

    return get_compile_context() == constants.CompileContext.DEPLOY  # pyright: ignore [reportPrivateImportUsage]


def get_backend_url(relative_url: str | Var[str]) -> Var[str]:
    """Get the full backend URL for a given relative URL.

    Use with `fetch` to access backend API endpoints.

    Args:
        relative_url: The relative URL to convert.

    Returns:
        A Var representing the full backend URL.
    """
    return ArgsFunctionOperation.create(
        args_names=("url",),
        return_expr=Var(
            r"`${getBackendURL(UPLOADURL).origin}/${url.replace(/^\/+/, '')}`"
        ),
        _var_data=VarData(
            imports={
                "$/utils/state": [
                    "getBackendURL",
                    "UPLOADURL",
                ],
            }
        ),
    )(relative_url).to(str)


def fetch(
    url: str | Var[str], options: dict[str, Any] | Var[dict[str, Any]] | None = None
) -> PromiseVar:
    """Fetch a URL with the given options.

    Args:
        url: The URL to fetch.
        options: The options to use for the fetch.

    Returns:
        A PromiseVar representing the eventual result of the fetch.
    """
    return ArgsFunctionOperationPromise.create(
        args_names=("url", "options"),
        return_expr=Var(
            "fetch(url, {...options, headers: {...options.headers, 'X-Reflex-Client-Token': token}})"
        ),
        _var_data=VarData(
            imports={
                "$/utils/state": [
                    "token",
                ],
            }
        ),
    )(url, options or {})


def encode_uri_component(value: str | Var[str]) -> Var[str]:
    """Encode a URI component.

    Args:
        value: The value to encode.

    Returns:
        A Var representing the encoded URI component.
    """
    return FunctionStringVar.create("encodeURIComponent")(value).to(str)


def arrow_func(py_fn: Callable) -> ArgsFunctionOperation:
    """Convert a Python function to a js arrow function."""
    sig = inspect.signature(py_fn)
    params = [
        Var(
            param.name,
            _var_type=param.annotation,
        ).guess_type()
        for param in sig.parameters.values()
    ]
    return ArgsFunctionOperation.create(
        args_names=tuple(sig.parameters),
        return_expr=py_fn(*params),
    )
