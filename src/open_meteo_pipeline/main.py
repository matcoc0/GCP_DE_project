from __future__ import annotations

import argparse

from .config import (
    build_api_url,
    load_api_configuration,
    load_hourly_variables,
)


def run_exploration(arguments: argparse.Namespace) -> None:
    """Run the exploration workflow."""

    geocoding_configuration = load_api_configuration("geocoding")
    weather_configuration = load_api_configuration("weather")
    air_quality_configuration = load_api_configuration("air_quality")

    weather_variables = load_hourly_variables("weather")
    air_quality_variables = load_hourly_variables("air_quality")

    print("\nOpen-Meteo exploration configuration")
    print("------------------------------------")
    print(f"City: {arguments.city}")
    print(f"Country code: {arguments.country_code or 'not specified'}")
    print(f"Forecast days: {arguments.forecast_days}")

    print("\nAPI endpoints")
    print(f"Geocoding: {build_api_url('geocoding')}")
    print(f"Weather: {build_api_url('weather')}")
    print(f"Air quality: {build_api_url('air_quality')}")

    print("\nRequest methods")
    print(f"Geocoding: {geocoding_configuration['request_method']}")
    print(f"Weather: {weather_configuration['request_method']}")
    print(f"Air quality: {air_quality_configuration['request_method']}")

    print("\nHourly variables")
    print(f"Weather: {', '.join(weather_variables)}")
    print(f"Air quality: {', '.join(air_quality_variables)}")


def main(arguments: argparse.Namespace) -> None:
    """Route the selected command to its workflow."""

    if arguments.command == "explore":
        run_exploration(arguments)
        return

    raise ValueError(f"Unsupported command: {arguments.command}")
