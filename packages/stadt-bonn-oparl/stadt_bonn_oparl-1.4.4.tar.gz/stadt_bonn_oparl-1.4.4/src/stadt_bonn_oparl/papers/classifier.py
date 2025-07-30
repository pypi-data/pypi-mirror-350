import json

import rich
from loguru import logger
from pydantic import DirectoryPath, FilePath

from stadt_bonn_oparl.agents.paper_classifier import analyze_document
from stadt_bonn_oparl.papers.models import Paper


def analyse_paper(data_path: DirectoryPath | FilePath, all: bool = False) -> bool:
    """
    Analyse a Markdown file and return the classification result.

    Parameters
    ----------
    data_path : DirectoryPath | FilePath
        Path to the markdown file or directory.
    all: bool
        If True, convert all PDFs in the directory

    """
    if all:
        for paper in data_path.glob("**/*.md"):
            _analyse_paper(paper)
    else:
        if not data_path.is_file() or not data_path.suffix == ".md":
            logger.error("The provided path is not a Markdown file.")
            return False

        _analyse_paper(data_path)

    logger.debug("OParl data conversion completed.")

    return True


def _analyse_paper(data_path: FilePath) -> bool:
    """
    Analyse a single markdown file.
    """
    logger.debug(f"Analysing paper: {data_path}")

    content = None
    metadata = None

    # Check if we have an analysis file already
    analysis_file = data_path.parent / "analysis.json"
    if analysis_file.exists():
        logger.info(f"Analysis file already exists: {analysis_file}")
        return True

    # Read the markdown file
    with open(data_path, "r", encoding="utf-8") as f:
        content = f.read()

    with open(data_path.parent / "metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    if content is None:
        logger.error(f"Failed to read file: {data_path}")
        return False

    analysis = analyze_document(
        Paper(id=metadata.get("id"), content=content, metadata=metadata)
    )

    if analysis is None:
        logger.error(f"Failed to analyze file: {data_path}")
        return False

    # save the analysis result to a JSON file
    with open(analysis_file, "w", encoding="utf-8") as f:
        f.write(analysis.model_dump_json())

    # use Rich to pretty print the result
    rich.print(analysis)

    return True
