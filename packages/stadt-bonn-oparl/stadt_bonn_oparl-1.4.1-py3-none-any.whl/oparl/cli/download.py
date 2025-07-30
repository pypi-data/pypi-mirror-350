from cyclopts import App
import logfire
from loguru import logger
from pydantic import DirectoryPath

from stadt_bonn.oparl.config import OPARL_BASE_URL, OPARL_PAPERS_ENDPOINT
from stadt_bonn.oparl.processors import download_oparl_pdfs


download = App(name="download", help="Download OPARL artifacts")


@download.command(name="paper")
def download_paper(data_path: DirectoryPath, start_page: int = 1, max_pages: int = 2):
    """
    Process OParl data and download PDFs.
    """
    logger.info("Starting OParl data processing...")

    oparl_url = f"{OPARL_BASE_URL}{OPARL_PAPERS_ENDPOINT}"

    logger.debug(
        f"Downloading OParl data from {oparl_url}, starting at page {start_page} and ending after {max_pages} pages at {start_page+max_pages}..."
    )
    with logfire.span(f"downloading OParl data from {oparl_url}"):
        total_downloads, actual_pdfs, html_pages = download_oparl_pdfs(
            oparl_url,
            start_page=start_page,
            max_pages=max_pages,
            data_path=data_path,
        )

    logger.info(
        f"OParl processing finished. Downloaded {total_downloads} files: "
        f"{actual_pdfs} actual PDFs, {html_pages} HTML pages"
    )

    if html_pages > 0 and actual_pdfs == 0:
        logger.warning(
            "No actual PDFs were downloaded. The documents appear to be behind an authentication wall. "
            "You may need to obtain access credentials to download the actual PDFs."
        )

    return True
