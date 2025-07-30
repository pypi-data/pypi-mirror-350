import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

import httpx
import requests
from loguru import logger

from .config import CACHE_DIR, USER_AGENT


def sanitize_name(name_str: str, is_url=False) -> str:
    """
    Sanitizes a string to be used as a valid directory or file name.
    If is_url is True, it performs more aggressive sanitization for URLs.
    """
    if not name_str:
        return "untitled"

    if is_url:
        # Remove http(s)://
        name_str = re.sub(r"^https?://", "", name_str)
        # Replace common URL characters with underscores
        name_str = re.sub(r"[/:?=&%#]", "_", name_str)

    # Remove or replace characters not allowed in filenames/paths
    # Keep alphanumeric, underscores, hyphens, and periods.
    name_str = re.sub(r"[^\w\-\.]", "_", name_str)
    # Replace multiple underscores/hyphens with a single one
    name_str = re.sub(r"[_]+", "_", name_str)
    name_str = re.sub(r"[-]+", "-", name_str)
    # Remove leading/trailing underscores/hyphens/periods
    name_str = name_str.strip("_-. ")
    # Limit length (optional, but good practice)
    return name_str[:100] if len(name_str) > 100 else name_str


def is_pdf_content(content):
    """
    Check if content is a PDF file.

    Args:
        content (bytes): The content to check

    Returns:
        bool: True if content appears to be a PDF, False otherwise
    """
    # Check for PDF magic number/header (%PDF-)
    if content and len(content) > 4 and content[:4] == b"%PDF":
        return True
    return False


def download_file(
    url: str, target_path: Path, item_title: str = "file", check_pdf=False
):
    """
    Downloads a file from a URL to a target path.

    Args:
        url (str): The URL to download from
        target_path (Path): The path to save the file to
        item_title (str): A description of the item being downloaded
        check_pdf (bool): Whether to check if the content is actually a PDF

    Returns:
        tuple: (bool success, str content_type) where success indicates if download was successful
               and content_type indicates what kind of content was downloaded ('pdf', 'html', 'other')
    """
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, stream=True, timeout=30, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Get full content for checking
        content = response.content
        content_type = "other"

        # Check content type if needed
        if check_pdf:
            if is_pdf_content(content):
                content_type = "pdf"
            elif b"<!DOCTYPE html>" in content[:100] or b"<html" in content[:100]:
                content_type = "html"
                logger.warning(f"Downloaded content is HTML, not PDF: {url}")

        target_path.parent.mkdir(parents=True, exist_ok=True)

        if content_type == "pdf":
            with open(target_path, "wb") as f:
                f.write(content)

            logger.info(f"Successfully downloaded {item_title}: {url} to {target_path}")

        return True, content_type
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading {item_title} from {url}: {e}")
    except IOError as e:
        logger.error(f"Error saving {item_title} to {target_path}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while downloading {url}: {e}")
    return False, "error"


def fetch_url_data(
    url: str, session: Optional[requests.Session] = None
) -> tuple[int, int, int, Optional[Dict[str, Any]]]:
    """Fetches JSON data from a single URL, using a local cache and updating metrics."""
    # Metrics
    CACHE_HITS = 0
    CACHE_MISSES = 0
    BYTES_FETCHED_NETWORK = 0

    # Ensure cache directory exists; create if not.
    # This is done here to avoid side effects on module import and handle it lazily.
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(
            f"Warning: Could not create cache directory {CACHE_DIR}. Caching disabled. Error: {e}"
        )
        # Fallback to non-cached behavior if directory creation fails
        try:
            requester = session or requests
            response = requester.get(url, timeout=10)
            response.raise_for_status()
            return CACHE_HITS, CACHE_MISSES, BYTES_FETCHED_NETWORK, response.json()
        except requests.exceptions.RequestException as req_e:
            print(
                f"Warning: Could not fetch data from {url} (no cache). Error: {req_e}"
            )
            return CACHE_HITS, CACHE_MISSES, BYTES_FETCHED_NETWORK, None
        except (
            json.JSONDecodeError
        ) as json_e:  # If server returns non-JSON for a 200 response
            print(
                f"Warning: Could not decode JSON from {url} (no cache). Error: {json_e}"
            )
            return CACHE_HITS, CACHE_MISSES, BYTES_FETCHED_NETWORK, None

    hashed_url = hashlib.md5(url.encode("utf-8")).hexdigest()
    cache_file_path = CACHE_DIR / f"{hashed_url}.json"

    # 1. Try to load from cache
    if cache_file_path.exists():
        try:
            with open(cache_file_path, "r", encoding="utf-8") as f:
                # print(f"Cache hit: Loading data for {url} from {cache_file_path}") # Optional: for debugging
                CACHE_HITS += 1
                return CACHE_HITS, CACHE_MISSES, BYTES_FETCHED_NETWORK, json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(
                f"Warning: Cache file {cache_file_path} for {url} is corrupted or unreadable. Refetching. Error: {e}"
            )
            # Attempt to delete corrupted cache file
            if cache_file_path.exists():  # Check again before deleting
                try:
                    os.remove(cache_file_path)
                except OSError as del_e:
                    print(
                        f"Warning: Could not delete corrupted cache file {cache_file_path}. Error: {del_e}"
                    )

    # 2. If not in cache or cache read failed, fetch from network
    # print(f"Cache miss: Fetching data for {url} from network.") # Optional: for debugging
    try:
        requester = session or requests
        response = requester.get(url, timeout=10)
        response.raise_for_status()
        # Collect metrics before trying to parse JSON, in case of non-JSON response
        CACHE_MISSES += 1
        BYTES_FETCHED_NETWORK += len(response.content)
        data = response.json()

        # 3. Save to cache
        try:
            with open(cache_file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # print(f"Cached: Saved data for {url} to {cache_file_path}") # Optional: for debugging
        except IOError as e:
            print(
                f"Warning: Could not write cache file {cache_file_path} for {url}. Error: {e}"
            )
        return CACHE_HITS, CACHE_MISSES, BYTES_FETCHED_NETWORK, data
    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not fetch data from {url}. Error: {e}")
        return CACHE_HITS, CACHE_MISSES, BYTES_FETCHED_NETWORK, None
    except json.JSONDecodeError as e:  # If server returns non-JSON for a 200 response
        print(
            f"Warning: Could not decode JSON from {url}, even after successful fetch. Error: {e}"
        )
        return CACHE_HITS, CACHE_MISSES, BYTES_FETCHED_NETWORK, None


def extract_id_from_oparl_url(full_url: str) -> Optional[str]:
    """
    Extract the object ID from an OParl object URL.
    Example: "https://www.bonn.sitzung-online.de/public/oparl/paper/12345" -> "12345"
    """
    try:
        parsed_url = httpx.URL(full_url)
        path_segments = [segment for segment in parsed_url.path.split("/") if segment]
        if path_segments:
            extracted_id = path_segments[-1]
            if extracted_id.isdigit():
                return extracted_id
            query_id = parsed_url.params.get("id")
            if query_id:
                return query_id
        else:
            query_id = parsed_url.params.get("id")
            if query_id:
                return query_id
    except Exception as e:
        logger.error(f"Error extracting ID from OParl URL {full_url}: {e}")
    return None
