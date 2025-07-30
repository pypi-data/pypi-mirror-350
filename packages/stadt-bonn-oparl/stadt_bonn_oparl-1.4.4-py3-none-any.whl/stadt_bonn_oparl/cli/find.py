from pathlib import Path

from cyclopts import App
from loguru import logger
from pydantic import DirectoryPath, NewPath


find = App("find", help="Find OPARL Papers")


@find.command(name="failed-downloads")
def find_failed_downloads(
    data_path: DirectoryPath, save_to_file: NewPath = Path("failed_downloads.json")
) -> bool:
    """
    Find all failed downloads in the specified directory.

    Parameters
    ----------
    data_path: DirectoryPath
        The path to the directory to search for failed downloads.
    save_to_file: FilePath
        The path to the file where the failed downloads will be saved.

    Returns
    -------
        bool: True if failed downloads are found, False otherwise.
    """
    logger.debug(f"Searching for failed downloads in {data_path}...")

    required_downloads = list(data_path.glob("**/metadata.json"))
    failed_downloads = []

    logger.debug(f"Found {len(required_downloads)} required downloads.")

    for download in required_downloads:
        # if there is a PDF file in the same directory as the metadata.json file
        # and the PDF file is not empty
        pdf_files = list(download.parent.glob("*.pdf"))
        if pdf_files:
            for pdf_file in pdf_files:
                if pdf_file.stat().st_size == 0:
                    logger.debug(f"Found failed download: {download}")
                    failed_downloads.append(download)
        else:
            # if there is no PDF file in the same directory as the metadata.json file
            failed_downloads.append(download)
            logger.debug(f"Download not found: {download}")

    if failed_downloads:
        logger.info(f"Found {len(failed_downloads)} failed downloads.")
        # write the failed downloads to a file, as JSON
        with open(save_to_file, "w", encoding="utf-8") as file:
            file.write("[\n")
            for download in failed_downloads:
                file.write(f'  "{download}",\n')
            file.write("]\n")

        return True

    logger.info("No failed downloads found.")
    return False


@find.command(name="unconverted-papers")
def find_unconverted_papers(
    data_path: DirectoryPath, save_to_file: NewPath = Path("unconverted_papers.json")
) -> bool:
    """
    Find all unconverted papers in the specified directory.

    Parameters
    ----------
    data_path: DirectoryPath
        The path to the directory to search for unconverted papers.
    save_to_file: FilePath
        The path to the file where the unconverted papers will be saved.

    Returns
    -------
        bool: True if unconverted papers are found, False otherwise.
    """
    logger.debug(f"Searching for unconverted papers in {data_path}...")

    unconverted_papers = []

    # for each subdirectory in data_path
    for subdir in data_path.iterdir():
        if subdir.is_dir():
            # check if a PDF is present
            pdf_files = list(subdir.glob("*.pdf"))
            if pdf_files:
                # check if the is a coresponding Markdown file
                md_files = list(subdir.glob("*.md"))
                if not md_files:
                    # if there is no Markdown file, add the PDF to the list of unconverted papers
                    logger.debug(f"Found unconverted paper: {subdir}")
                    unconverted_papers.append({"data_path": subdir.as_posix()})

    if unconverted_papers:
        logger.info(f"Found {len(unconverted_papers)} unconverted papers.")
        # write the failed downloads to a file, as JSON
        with open(save_to_file, "w", encoding="utf-8") as file:
            file.write("[\n")
            for download in unconverted_papers:
                file.write(f'  "{download}",\n')
            file.write("]\n")

        return True

    logger.info("No unconverted papers found.")
    return False


@find.command(name="missing-analysis")
def find_missing_analysis(
    data_path: DirectoryPath, save_to_file: NewPath = Path("missing_analysis.json")
) -> bool:
    """
    Find all missing analysis in the specified directory.

    Parameters
    ----------
    data_path: DirectoryPath
        The path to the directory to search for missing analysis.
    save_to_file: FilePath
        The path to the file where the missing analysis will be saved.

    Returns
    -------
        bool: True if missing analysis are found, False otherwise.
    """
    logger.debug(f"Searching for missing analysis in {data_path}...")

    missing_analysis = []

    # for each subdirectory in data_path we want to check if there is an Markdown file
    # and a corresponding analysis file
    for subdir in data_path.iterdir():
        if subdir.is_dir():
            # check if a Markdown file is present
            md_files = list(subdir.glob("*.md"))
            if md_files:
                # check if the is a coresponding analysis file
                analysis_files = subdir / "analysis.json"
                if not analysis_files.exists():
                    logger.debug(f"Found missing analysis: {subdir}")
                    missing_analysis.append({"data_path": subdir.as_posix()})

    if missing_analysis:
        logger.info(f"Found {len(missing_analysis)} missing analysis.")
        # write the failed downloads to a file, as JSON
        with open(save_to_file, "w", encoding="utf-8") as file:
            file.write("[\n")
            for download in missing_analysis:
                file.write(f'  "{download}",\n')
            file.write("]\n")

        return True

    logger.info("No missing analysis found.")
    return False
