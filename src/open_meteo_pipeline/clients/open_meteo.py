from __future__ import annotations

from typing import Any

import httpx

from ..config import (
    build_api_url,
    load_api_configuration,
    load_hourly_variables,
)
from .http_client import request_json


def geocode_city(
    client: httpx.Client, *, city: str, country_code: str | None = None
) -> dict[str, Any]:
    """Resolve a city name into Open-Meteo location metadata."""

    configuration = load_api_configuration("geocoding")

    params: dict[str, Any] = {
        **configuration["default_params"],
        "name": city,
    }

    if country_code:
        params["countryCode"] = country_code.upper()

    payload = request_json(
        client,
        method=configuration["request_method"],
        url=build_api_url("geocoding"),
        params=params,
    )

    results = payload.get("results", [])

    if not isinstance(results, list) or not results:
        raise ValueError(f"No location found for city: {city}")

    location = results[0]

    if not isinstance(location, dict):
        raise ValueError("Invalid geocoding result")

    required_fields = {
        "id",
        "name",
        "latitude",
        "longitude",
        "timezone",
        "country_code",
    }

    missing_fields = required_fields - location.keys()

    if missing_fields:
        raise ValueError(
            "Geocoding result is missing required fields: f{sorted(missing_fields)}"
        )

    return location


def fetch_weather(
    client: httpx.Client, *, latitude: float, longitude: float, forecast_days: int
) -> dict[str, Any]:
    """Fetch hourly weather forecasts."""

    configuration = load_api_configuration("weather")

    params = {
        **configuration["default_params"],
        "latitude": latitude,
        "longitude": longitude,
        "forecast_days": forecast_days,
        "hourly": ",".join(load_hourly_variables("weather")),
    }

    return request_json(
        client,
        method=configuration["request_method"],
        url=build_api_url("weather"),
        params=params,
    )


def fetch_air_quality(
    client: httpx.Client,
    *,
    latitude: float,
    longitude: float,
    forecast_days: int,
) -> dict[str, Any]:
    """Fetch hourly air-quality forecasts."""

    configuration = load_api_configuration("air_quality")

    params = {
        **configuration["default_params"],
        "latitude": latitude,
        "longitude": longitude,
        "forecast_days": forecast_days,
        "hourly": ",".join(load_hourly_variables("air_quality")),
    }

    return request_json(
        client,
        method=configuration["request_method"],
        url=build_api_url("air_quality"),
        params=params,
    )
