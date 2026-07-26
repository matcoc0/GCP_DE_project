from __future__ import annotations

import json
from pathlib import Path

import pytest

from open_meteo_pipeline.config.loader import (
    build_api_url,
    load_api_configuration,
    load_hourly_variables,
    load_json_configuration,
)


def test_load_json_configuration_returns_dictionary(
    tmp_path: Path,
) -> None:
    configuration_path = tmp_path / "configuration.json"
    configuration_path.write_text(
        json.dumps({"source": {"enabled": True}}),
        encoding="utf-8",
    )

    result = load_json_configuration(configuration_path)

    assert result == {"source": {"enabled": True}}


def test_load_json_configuration_rejects_missing_file(
    tmp_path: Path,
) -> None:
    configuration_path = tmp_path / "missing.json"

    with pytest.raises(
        FileNotFoundError,
        match="Configuration file not found",
    ):
        load_json_configuration(configuration_path)


def test_load_json_configuration_rejects_invalid_json(
    tmp_path: Path,
) -> None:
    configuration_path = tmp_path / "invalid.json"
    configuration_path.write_text(
        '{"weather": ',
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Invalid JSON configuration file",
    ):
        load_json_configuration(configuration_path)


def test_load_json_configuration_rejects_non_object_root(
    tmp_path: Path,
) -> None:
    configuration_path = tmp_path / "list.json"
    configuration_path.write_text(
        '["weather", "air_quality"]',
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Configuration root must be a JSON object",
    ):
        load_json_configuration(configuration_path)


def test_load_weather_api_configuration() -> None:
    configuration = load_api_configuration("weather")

    assert configuration["request_method"] == "GET"
    assert configuration["endpoint"] == "/v1/forecast"
    assert configuration["default_params"]["timezone"] == "UTC"


def test_load_api_configuration_rejects_unknown_api() -> None:
    with pytest.raises(
        KeyError,
        match="Unknown API configuration",
    ):
        load_api_configuration("unknown")


def test_load_weather_hourly_variables() -> None:
    variables = load_hourly_variables("weather")

    assert "temperature_2m" in variables
    assert "precipitation" in variables


def test_load_air_quality_hourly_variables() -> None:
    variables = load_hourly_variables("air_quality")

    assert "pm10" in variables
    assert "european_aqi" in variables


def test_build_weather_api_url() -> None:
    result = build_api_url("weather")

    assert result == "https://api.open-meteo.com/v1/forecast"


def test_build_air_quality_api_url() -> None:
    result = build_api_url("air_quality")

    assert result == ("https://air-quality-api.open-meteo.com/v1/air-quality")
