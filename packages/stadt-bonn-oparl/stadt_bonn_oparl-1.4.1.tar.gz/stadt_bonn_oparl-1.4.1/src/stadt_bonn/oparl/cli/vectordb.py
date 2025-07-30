import json

from cyclopts import App
from loguru import logger
from pydantic import DirectoryPath

from stadt_bonn.oparl.papers.models import UnifiedPaper
from stadt_bonn.oparl.papers.vector_db import VectorDb

vectordb = App(name="vectordb", help="Ingest OPARL Papers into VectorDB")


@vectordb.command()
def ingest(data_path: DirectoryPath, vectordb_name: str) -> bool:
    """
    Ingest OPARL Papers, including metadata, analysis and content, to VectorDB.

    Parameters
    ----------
    data_path: DirectoryPath
        Path to the directory containing OPARL Papers in PDF file
    vector_db_name: str
        Name of the VectorDB to ingest data into
    """
    db = VectorDb(vectordb_name)

    # Check if the directory exists
    if not data_path.exists():
        logger.error(f"Directory {data_path} does not exist.")
        return False

    for dir_path in data_path.iterdir():
        try:
            rats_info = _create_paper(dir_path)
            doc_id = db.create_document(rats_info)
            logger.debug(f"Document created with ID: {doc_id}")
        except FileNotFoundError as e:
            logger.error(e)

    return True


def _create_paper(data_path: DirectoryPath) -> UnifiedPaper:
    """
    Create a Paper object from a directory path.
    """
    # Assuming the directory contains metadata.json and content.txt files
    metadata_path = data_path / "metadata.json"
    analysis_path = data_path / "analysis.json"
    content_path = data_path.glob("*.md")  # Get the first markdown file
    content = ""
    analysis = {}
    metadata = {}

    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found in {data_path}")
    if not content_path:
        raise FileNotFoundError(f"No markdown files found in {data_path}")

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    with open(analysis_path, "r") as f:
        analysis = json.load(f)

    for file in content_path:
        if file.suffix == ".md":
            with open(file, "r") as f:
                content = f.read()

    return UnifiedPaper(
        paper_id=metadata.get("id"),
        metadata=metadata,
        markdown_text=content,
        analysis=analysis,
        enrichment_status="enriched",
        external_oparl_data={},
    )
