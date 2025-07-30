from dataclasses import dataclass
from enum import Enum
import os
import typer
from rich.console import Console
from typing import Tuple

console = Console()


class EnvEnum(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


@dataclass
class EnvironmentConfig:
    zenetics_key: str
    env: EnvEnum
    zenetics_api_url: str
    zenetics_portal_url: str

    def __str__(self):
        return "Environment: ***"


def validate_environment() -> EnvironmentConfig:
    """Validate required environment variables."""
    zenetics_key = os.getenv("ZENETICS_API_KEY")
    environment = os.getenv("ENV")

    if not environment:
        # Default to prod
        environment = EnvEnum.PROD

    missing_vars = []
    if not zenetics_key:
        missing_vars.append("ZENETICS_API_KEY")

    if missing_vars:
        console.print(
            f"[red]Error: Missing required environment "
            f"variables: {', '.join(missing_vars)}"
        )
        console.print("\nPlease set the following environment variables:")
        console.print("  export ZENETICS_API_KEY=your_api_key")
        raise typer.Exit(1)

    zenetics_api_url, zenetics_portal_url = get_zenetics_urls(environment)

    return EnvironmentConfig(
        zenetics_key=zenetics_key,
        env=environment,
        zenetics_api_url=zenetics_api_url,
        zenetics_portal_url=zenetics_portal_url,
    )


def get_zenetics_urls(env: EnvEnum) -> Tuple[str, str]:
    """
    Get Zenetics API and Portal URLs based on environment.

    Returns:
        Tuple[str, str]: Zenetics API and Portal URL
    """
    if env == EnvEnum.LOCAL:
        return "http://localhost:8080", "http://localhost:3000"
    elif env == EnvEnum.DEV:
        return "https://dev.api.zenetics.io", "https://dev.app.zenetics.io"
    elif env == EnvEnum.STAGING:
        return "https://staging.api.zenetics.io", "https://staging.app.zenetics.io"
    elif env == EnvEnum.PROD:
        return "https://api.zenetics.io", "https://app.zenetics.io"
    else:
        raise ValueError(f"Invalid environment: {env}")
