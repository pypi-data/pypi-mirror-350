from cyclopts import App
from loguru import logger
from pydantic import DirectoryPath, FilePath

from stadt_bonn_oparl.processors import convert_oparl_pdf


convert = App(
    name="convert", help="Convert OPARL Papers PDF to Markdown and Docling format"
)


@convert.command(name=["paper", "papers"])
def convert_paper(data_path: DirectoryPath | FilePath, all: bool = False) -> bool:
    """
    Convert an OPARL Papers PDF to Markdown and Docling format.
    This function processes a single PDF file or all PDFs in the specified directory.

    Parameters
    ----------
    data_path: DirectoryPath | FilePath
        Path to the directory containing OPARL Papers in PDF file
    all: bool
        If True, convert all PDFs in the directory

    Returns
    -------
        bool: True if conversion is successful, False otherwise
    """

    if all:
        # Convert all PDFs in the directory
        # Assuming convert_oparl_pdf saves to CONVERTED_DATA_DIRECTORY
        for pdf_file in data_path.glob("**/*.pdf"):
            convert_oparl_pdf(pdf_file, data_path=pdf_file.parent)
    else:
        # Convert a single PDF file
        if not data_path.is_file() or not data_path.suffix == ".pdf":
            logger.error("The provided path is not a valid PDF file.")
            return False

        convert_oparl_pdf(data_path, data_path=data_path.parent)

    logger.debug("OParl data conversion completed.")

    return True
