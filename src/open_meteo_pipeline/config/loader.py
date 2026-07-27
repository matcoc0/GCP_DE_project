from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONFIGURATION_DIRECTORY = PROJECT_ROOT / "configurations"

API_CONFIGURATION_PATH = CONFIGURATION_DIRECTORY / "APIs.json"
VARIABLE_CONFIGURATION_PATH = CONFIGURATION_DIRECTORY / "variables.json"

REQUIRED_API_FIELDS = {
    "base_url",
    "endpoint",
    "request_method",
    "timeout_seconds",
    "default_params",
}


def load_json_configuration(path: Path) -> dict[str, Any]:
    """Load a JSON configuration file and validate its root structure."""

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Configuration path is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON configuration file: {path}") from error

    if not isinstance(payload, dict):
        raise ValueError(f"Configuration root must be a JSON object: {path}")

    return payload


def load_api_configurations() -> dict[str, Any]:
    """Load all API configurations."""

    return load_json_configuration(API_CONFIGURATION_PATH)


def load_api_configuration(api_name: str) -> dict[str, Any]:
    """Load and validate one API configuration."""

    configurations = load_api_configurations()

    try:
        configuration = configurations[api_name]
    except KeyError as error:
        available_apis = ", ".join(sorted(configurations))

        raise KeyError(
            f"Unknown API configuration: {api_name}. Available APIs: {available_apis}"
        ) from error

    if not isinstance(configuration, dict):
        raise ValueError(f"API configuration must be an object: {api_name}")

    missing_fields = REQUIRED_API_FIELDS - configuration.keys()

    if missing_fields:
        raise ValueError(
            f"API configuration '{api_name}' is missing fields: "
            f"{sorted(missing_fields)}"
        )

    request_method = configuration["request_method"]

    if not isinstance(request_method, str):
        raise ValueError(f"API request method must be a string: {api_name}")

    if request_method.upper() not in {"GET", "POST"}:
        raise ValueError(
            f"Unsupported API request method for '{api_name}': {request_method}"
        )

    default_params = configuration["default_params"]

    if not isinstance(default_params, dict):
        raise ValueError(f"default_params must be an object for API: {api_name}")

    return configuration


def load_variable_configurations() -> dict[str, Any]:
    """Load all variable configurations."""

    return load_json_configuration(VARIABLE_CONFIGURATION_PATH)


def load_hourly_variables(source_name: str) -> list[str]:
    """Load hourly variables for a weather or air-quality source."""

    configurations = load_variable_configurations()

    try:
        source_configuration = configurations[source_name]
    except KeyError as error:
        available_sources = ", ".join(sorted(configurations))

        raise KeyError(
            f"Unknown variable configuration: {source_name}."
            f"Available sources: {available_sources}"
        ) from error

    if not isinstance(source_configuration, dict):
        raise ValueError(f"Variable configuration must be an object: {source_name}")

    hourly_variables = source_configuration.get("hourly")

    if not isinstance(hourly_variables, list):
        raise ValueError(f"Hourly variables must be a list for source: {source_name}")

    if not hourly_variables:
        raise ValueError(f"Hourly variables cannot be empty for source: {source_name}")

    if not all(
        isinstance(variable, str) and variable.strip() for variable in hourly_variables
    ):
        raise ValueError(
            f"Hourly variables must contain non-empty strings: {source_name}"
        )

    return hourly_variables


def build_api_url(api_name: str) -> str:
    """Build the complete URL for a configured API."""

    configuration = load_api_configuration(api_name)

    base_url = str(configuration["base_url"]).rstrip("/")
    endpoint = str(configuration["endpoint"])

    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"

    return f"{base_url}{endpoint}"
