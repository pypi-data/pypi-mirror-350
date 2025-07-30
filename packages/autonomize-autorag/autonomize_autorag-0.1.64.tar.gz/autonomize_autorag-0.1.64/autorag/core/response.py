""" This module contains utility functions for the modelhub package. """

from typing import Any, Dict

import httpx

from autorag.utilities.logger import get_logger

logger = get_logger(__name__)


def handle_response(response: httpx.Response) -> Dict[str, Any]:
    """
    Synchronously handle the response from an HTTP request.

    Args:
        response (httpx.Response): The response object from the HTTP request.

    Returns:
        dict: The JSON response from the HTTP request.

    Raises:
        httpx.HTTPError: If the HTTP response status code is an error.
        ValueError: If the response is not a valid JSON.
    """
    try:
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        logger.error("HTTP error: %s", str(e))
        raise
    except ValueError as e:
        logger.error("Invalid JSON response: %s", str(e))
        raise


async def ahandle_response(response: httpx.Response) -> Dict[str, Any]:
    """
    Asynchronously handles the response from an HTTP request.

    Args:
        response (httpx.Response): The response object from the HTTP request.

    Returns:
        dict: The JSON response from the HTTP request.

    Raises:
        httpx.HTTPError: If the HTTP response status code is an error.
        ValueError: If the response is not a valid JSON.
    """
    try:
        response.raise_for_status()
        # Use sync version for simplicity - httpx.Response.json()
        # is not a coroutine in current versions
        return response.json()
    except httpx.HTTPError as e:
        logger.error("HTTP error: %s", str(e))
        raise
    except ValueError as e:
        logger.error("Invalid JSON response: %s", str(e))
        raise
