from __future__ import annotations

from typing import Any


def inspect_hourly_data(
    payload: dict[str, Any],
    source_name: str,
) -> None:
    """Validate and display an overview of hourly API data."""

    hourly = payload.get("hourly")
    hourly_units = payload.get("hourly_units")

    if not isinstance(hourly, dict):
        raise ValueError(f"{source_name}: missing or invalid hourly object")

    if not isinstance(hourly_units, dict):
        raise ValueError(f"{source_name}: missing or invalid hourly_units object")

    lengths = {
        variable: len(values)
        for variable, values in hourly.items()
        if isinstance(values, list)
    }

    if not lengths:
        raise ValueError(f"{source_name}: no hourly series found")

    if len(set(lengths.values())) != 1:
        raise ValueError(f"{source_name}: hourly series have different lengths")

    print(f"\n--- {source_name} ---")
    print(f"Top-level fields: {sorted(payload.keys())}")
    print(f"Hourly variables: {sorted(hourly.keys())}")
    print(f"Units: {hourly_units}")
    print(f"Hourly row count: {next(iter(lengths.values()))}")

    for variable, values in hourly.items():
        if isinstance(values, list):
            print(f"{variable}: {values[:3]}")


def display_location(location: dict[str, Any]) -> None:
    """Display the selected geocoding result."""

    print("\nSelected location")
    print(f"Name: {location['name']}")
    print(f"Country: {location.get('country')}")
    print(f"Country code: {location['country_code']}")
    print(f"Admin area: {location.get('admin1')}")
    print(f"Latitude: {location['latitude']}")
    print(f"Longitude: {location['longitude']}")
    print(f"Timezone: {location['timezone']}")
    print(f"Population: {location.get('population')}")
