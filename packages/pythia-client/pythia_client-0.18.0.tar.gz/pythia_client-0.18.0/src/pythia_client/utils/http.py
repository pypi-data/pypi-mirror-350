"""HTTP utilities for the API client."""

import json
from typing import Dict, Any


def create_headers(api_key: str) -> Dict[str, str]:
    """Create headers for API requests.

    Args:
        api_key: The API key for authentication.

    Returns:
        A dictionary of headers.
    """
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }


def create_basic_headers(api_key: str) -> Dict[str, str]:
    """Create basic headers for API requests without content type.

    Args:
        api_key: The API key for authentication.

    Returns:
        A dictionary of headers.
    """
    return {
        "X-API-Key": api_key,
    }


def prepare_json_payload(request_obj: Any) -> Dict[str, Any]:
    """Convert a request object to a JSON payload.

    Args:
        request_obj: The request object to convert.

    Returns:
        A dictionary representing the JSON payload.
    """
    return json.loads(request_obj.model_dump_json())
