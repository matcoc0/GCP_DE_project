from __future__ import annotations

import httpx

from .clients.open_meteo import (
    fetch_air_quality,
    fetch_weather,
    geocode_city,
)
from .config import load_api_configuration
from .services.exploration import (
    display_location,
    inspect_hourly_data,
)


def run_exploration(
    city: str, country_code: str | None = None, forecast_days: int = 3
) -> None:
    """Fetch and inspect Open-Meteo data."""
    normalized_city = city.strip()

    if not normalized_city:
        raise ValueError("city cannot be empty.")

    normalized_country_code = None

    if country_code:
        normalized_country_code = country_code.strip().upper()

        if len(normalized_country_code) != 2:
            raise ValueError("country_code must be a two-character ISO country code.")

    if not 1 <= forecast_days <= 7:
        raise ValueError("forecast_days must be between 1 and 7.")

    geocoding_configuration = load_api_configuration("geocoding")
    weather_configuration = load_api_configuration("weather")
    air_quality_configuration = load_api_configuration("air_quality")

    timeout_seconds = max(
        float(geocoding_configuration["timeout_seconds"]),
        float(weather_configuration["timeout_seconds"]),
        float(air_quality_configuration["timeout_seconds"]),
    )

    with httpx.Client(timeout=timeout_seconds, follow_redirects=True) as client:
        location = geocode_city(client, city=city, country_code=country_code)

        weather = fetch_weather(
            client,
            latitude=float(location["latitude"]),
            longitude=float(location["longitude"]),
            forecast_days=forecast_days,
        )

        air_quality = fetch_air_quality(
            client,
            latitude=float(location["latitude"]),
            longitude=float(location["longitude"]),
            forecast_days=forecast_days,
        )

    display_location(location)

    inspect_hourly_data(weather, source_name="weather")
    inspect_hourly_data(air_quality, source_name="air_quality")


def main(
    city: str,
    country_code: str | None = None,
    forecast_days: int = 3,
    unknown_args: list[str] | None = None,
) -> None:
    """Route the selected command to its workflow."""

    unknown_args = unknown_args or []
    if unknown_args:
        print(f"Unknown arguments ignored: {unknown_args}")

    run_exploration(city=city, country_code=country_code, forecast_days=forecast_days)
