"""Enterprise utilities for Reflex CLI."""

from typing import ClassVar

from reflex.config import Config, EnvironmentVariables, EnvVar, env_var


class ConfigEnterprise(Config):
    """Enterprise configuration class."""

    show_built_with_reflex: bool | None = None

    use_single_port: bool | None = None

    _prefixes: ClassVar[list[str]] = ["REFLEX_", "REFLEX_ENTERPRISE_"]


class EnvironmentEnterpriseVariables(EnvironmentVariables):
    """Enterprise environment variables."""

    # Set the access token needed to authenticate with the Reflex backend.
    REFLEX_ACCESS_TOKEN: EnvVar[str | None] = env_var(None)


Config = ConfigEnterprise

environment = EnvironmentEnterpriseVariables()
