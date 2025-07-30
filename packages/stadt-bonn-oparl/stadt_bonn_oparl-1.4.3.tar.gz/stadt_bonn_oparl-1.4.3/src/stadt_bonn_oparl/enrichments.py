import json
from typing import Any, Dict, List, Optional, Tuple

import requests
from loguru import logger
from pydantic import DirectoryPath

from stadt_bonn_oparl.papers.exceptions import PaperDataLoadError
from stadt_bonn_oparl.papers.models import UnifiedPaper
from stadt_bonn_oparl.utils import fetch_url_data

# Metrics
CACHE_HITS = 0
CACHE_MISSES = 0
BYTES_FETCHED_NETWORK = 0


def load_core_paper_files(
    paper_directory: DirectoryPath,
) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """
    Loads the core data files (metadata.json, analysis.json, and content.md)
    from the given paper directory.

    Args:
        paper_directory: The Path object pointing to the directory of a single paper.

    Returns:
        A tuple containing:
            - metadata_content (dict)
            - analysis_content (dict)
            - markdown_content (str)

    Raises:
        PaperDataLoadError: If any of the essential files are missing or cannot be parsed.
    """
    metadata_file = paper_directory / "metadata.json"
    analysis_file = paper_directory / "analysis.json"

    # Attempt to find the markdown file (assuming only one .md file per directory)
    markdown_files = list(paper_directory.glob("*.md"))
    if not markdown_files:
        raise PaperDataLoadError(f"No markdown file found in {paper_directory}")
    if len(markdown_files) > 1:
        # This case might need a more sophisticated selection logic if multiple MDs are expected
        logger.error(
            f"Warning: Multiple markdown files found in {paper_directory}. Using {markdown_files[0].name}"
        )
    markdown_file_path = markdown_files[0]

    if not metadata_file.exists():
        raise PaperDataLoadError(f"Missing metadata.json in {paper_directory}")
    if not analysis_file.exists():
        raise PaperDataLoadError(f"Missing analysis.json in {paper_directory}")
    if (
        not markdown_file_path.exists()
    ):  # Should be covered by glob, but good for clarity
        raise PaperDataLoadError(
            f"Missing markdown file {markdown_file_path.name} in {paper_directory}"
        )

    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata_content = json.load(f)
    except json.JSONDecodeError as e:
        raise PaperDataLoadError(
            f"Error decoding metadata.json in {paper_directory}: {e}"
        )
    except IOError as e:
        raise PaperDataLoadError(
            f"Error reading metadata.json in {paper_directory}: {e}"
        )

    try:
        with open(analysis_file, "r", encoding="utf-8") as f:
            analysis_content = json.load(f)
    except json.JSONDecodeError as e:
        raise PaperDataLoadError(
            f"Error decoding analysis.json in {paper_directory}: {e}"
        )
    except IOError as e:
        raise PaperDataLoadError(
            f"Error reading analysis.json in {paper_directory}: {e}"
        )

    try:
        with open(markdown_file_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
    except IOError as e:
        raise PaperDataLoadError(
            f"Error reading markdown file {markdown_file_path.name} in {paper_directory}: {e}"
        )

    return metadata_content, analysis_content, markdown_content


def enrich_with_external_data(
    metadata_content: Dict[str, Any],
) -> Tuple[Dict[str, Optional[Dict[str, Any]]], str]:
    """
    Enriches the paper data by fetching information from URLs listed in the metadata.

    Args:
        metadata_content: The dictionary loaded from metadata.json.

    Returns:
        A tuple containing:
            - A dictionary where keys are URLs and values are the fetched JSON data (or None if failed).
            - An enrichment_status string ("complete" or "incomplete_external_data").
    """
    external_data_store: Dict[str, Optional[Dict[str, Any]]] = {}
    enrichment_status = "complete"
    urls_to_fetch: List[str] = []

    # Extract URLs from various known fields
    if "originatorPerson" in metadata_content and isinstance(
        metadata_content["originatorPerson"], list
    ):
        urls_to_fetch.extend(metadata_content["originatorPerson"])

    if "underDirectionOf" in metadata_content and isinstance(
        metadata_content["underDirectionOf"], list
    ):
        urls_to_fetch.extend(metadata_content["underDirectionOf"])

    if "consultation" in metadata_content and isinstance(
        metadata_content["consultation"], list
    ):
        for consult_item in metadata_content["consultation"]:
            if isinstance(consult_item, dict):
                if "organization" in consult_item and isinstance(
                    consult_item["organization"], list
                ):
                    urls_to_fetch.extend(consult_item["organization"])
                if "meeting" in consult_item and isinstance(
                    consult_item["meeting"], str
                ):  # OParl spec says meeting is a URL string
                    urls_to_fetch.append(consult_item["meeting"])

    # Add other direct URL fields if any, e.g., 'body' or 'mainFile.accessUrl' if they point to OParl entities.
    # The 'id' of the paper itself, or 'mainFile.id' are also URLs but point to the current context or a file.

    unique_urls_to_fetch = sorted(
        list(
            set(
                u
                for u in urls_to_fetch
                if u and isinstance(u, str) and u.startswith("http")
            )
        )
    )

    if not unique_urls_to_fetch:
        logger.info("No valid external URLs found in metadata for enrichment.")
        return {}, enrichment_status  # No external URLs to fetch

    logger.debug(f"Found {len(unique_urls_to_fetch)} unique, valid URLs to fetch.")

    with (
        requests.Session() as session
    ):  # Use a session for potential connection pooling
        for url in unique_urls_to_fetch:
            logger.debug(f"Fetching: {url}")
            h, m, t, data = fetch_url_data(url, session)
            external_data_store[url] = data
            if data is None:  # _fetch_url_data returns None on failure
                enrichment_status = "incomplete_external_data"

    return external_data_store, enrichment_status


def consolidate_paper_data(
    metadata_content: Dict[str, Any],
    analysis_content: Dict[str, Any],
    markdown_content: str,
    external_data: Dict[str, Optional[Dict[str, Any]]],
    enrichment_status: str,
) -> UnifiedPaper:
    """
    Consolidates all loaded and enriched data into a single UnifiedPaperData object.
    """
    paper_id = metadata_content.get("reference")  # Prefer 'reference' if available
    if not paper_id:
        paper_id = metadata_content.get(
            "id", "MISSING_ID"
        )  # Fallback to 'id' or a placeholder

    return UnifiedPaper(
        paper_id=str(paper_id),  # Ensure it's a string
        metadata=metadata_content,
        analysis=analysis_content,
        markdown_text=markdown_content,
        external_oparl_data=external_data,
        enrichment_status=enrichment_status,
        # validation_status will be set later
    )
