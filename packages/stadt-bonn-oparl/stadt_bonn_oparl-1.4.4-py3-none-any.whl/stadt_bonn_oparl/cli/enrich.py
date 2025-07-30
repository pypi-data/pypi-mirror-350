from pathlib import Path

from cyclopts import App
from loguru import logger
from pydantic import DirectoryPath, NewPath

from stadt_bonn_oparl.enrichments import (
    consolidate_paper_data,
    enrich_with_external_data,
    load_core_paper_files,
)
from stadt_bonn_oparl.papers.exceptions import PaperDataLoadError

enrich = App(name="enrich", help="enrich a OPARL entity")


@enrich.command(name="paper")
def enrich_paper(data_path: DirectoryPath):
    """
    Enrich a OPARL paper in the specified directory.

    Parameters
    ----------
    data_path: DirectoryPath
        The path to the directory containing the OPARL paper.

    Returns
    -------
        bool: True if failed downloads are found, False otherwise.
    """
    logger.debug(f"Attempting to load data from: {data_path}")

    try:
        # Load core files
        metadata, analysis, md_text = load_core_paper_files(data_path)
        logger.debug("Successfully loaded core files.")

        # Enrich with external data
        external_data, enrichment_status = enrich_with_external_data(metadata)
        logger.debug(f"Enrichment Status: {enrichment_status}")
        successful_fetches = sum(1 for d in external_data.values() if d is not None)
        logger.debug(
            f"Successfully fetched data for {successful_fetches} out of {len(external_data)} URLs attempted."
        )

        # Consolidate data
        unified_paper = consolidate_paper_data(
            metadata_content=metadata,
            analysis_content=analysis,
            markdown_content=md_text,
            external_data=external_data,
            enrichment_status=enrichment_status,
        )
        logger.debug(f"Unified Paper ID: {unified_paper.paper_id}")
        logger.debug(
            f"Unified Paper Ingestion Status: {unified_paper.enrichment_status}"
        )
        logger.debug(
            f"Number of external data entries: {len(unified_paper.external_oparl_data)}"
        )
        logger.debug(f"Markdown length: {len(unified_paper.markdown_text)}")

        # Save the consolidated data to a file
        save_to_file: NewPath = Path(data_path) / "enriched.json"
        with open(save_to_file, "w", encoding="utf-8") as f:
            logger.debug(f"Saving enriched paper to {save_to_file}")
            f.write(unified_paper.model_dump_json(indent=2))
    except PaperDataLoadError as e:
        logger.exception(f"Error during ingestion process: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
