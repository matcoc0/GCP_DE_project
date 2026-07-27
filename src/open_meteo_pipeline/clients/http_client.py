from __future__ import annotations

from typing import Any

import httpx


def request_json(
    client: httpx.Client,
    *,
    method: str,
    url: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute an HTTP request and return a JSON object."""

    response = client.request(method=method.upper(), url=url, params=params)
    response.raise_for_status()

    payload = response.json()

    if not isinstance(payload, dict):
        raise ValueError(
            f"Unexpected response type from {url}: {type(payload).__name__}"
        )

    return payload
