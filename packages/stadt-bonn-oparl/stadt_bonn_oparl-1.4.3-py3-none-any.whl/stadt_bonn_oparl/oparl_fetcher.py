from typing import Any, Optional

import httpx
import logfire
from loguru import logger

from .config import OPARL_BASE_URL, USER_AGENT


logfire.instrument_httpx()


async def get_oparl_data(
    endpoint_path: str, params: Optional[dict[str, Any]] = None
) -> Optional[dict[str, Any]]:
    """
    Fetches data from the OParl API.

    Args:
        endpoint_path: The specific API endpoint path (e.g., "/system", "/papers").
        params: Optional dictionary of query parameters.

    Returns:
        A dictionary containing the JSON response if successful, None otherwise.
    """
    url = f"{OPARL_BASE_URL}{endpoint_path}"
    headers = {"User-Agent": USER_AGENT}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raises an HTTPStatusError for 4xx/5xx responses
            return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}"
            )
            return None
        except httpx.RequestError as exc:
            logger.error(
                f"An error occurred while requesting {exc.request.url!r}: {exc}"
            )
            return None
        except Exception as exc:
            logger.error(f"An unexpected error occurred: {exc}")
            return None


async def get_oparl_list_data(
    endpoint_path: str, params: Optional[dict[str, Any]] = None
) -> Optional[list[Any]]:
    """
    Fetches list data from the OParl API.

    Args:
        endpoint_path: The specific API endpoint path (e.g., "/papers").
        params: Optional dictionary of query parameters.

    Returns:
        A list containing the JSON response data if successful, None otherwise.
    """
    data = await get_oparl_data(endpoint_path, params)
    if data and "data" in data and isinstance(data["data"], list):
        return data["data"]
    elif data:  # if data is returned but not in the expected list format
        logger.warning(
            f"Expected list data from {endpoint_path} but got different format: {data}"
        )
        return []  # Return empty list to avoid breaking callers expecting a list
    return None
