from pathlib import Path

from cyclopts import App
from loguru import logger
from pydantic import DirectoryPath

from stadt_bonn_oparl.papers.models import TagAggregationPeriod
from stadt_bonn_oparl.papers.tag_aggregation import aggregate_tags_by_date

extract = App(
    name="extract", help="extract the word frequency from OPARL Papers analysis files"
)


@extract.command()
def wordfrequency(
    data_path: DirectoryPath,
    save_to_file: Path = Path("word_frequency.json"),
    force_overwrite: bool = False,
    aggregate: TagAggregationPeriod = TagAggregationPeriod.DAILY,
):
    """
    Analyze the word frequency in OPARL Papers analysis files.


    Parameters
    ----------
    data_path: DirectoryPath
        Path to the directory containing OPARL Papers analysis files
    save_to_file: NewPath
        Path to the file where the word frequency data will be saved
    force_overwrite: bool
        If True, overwrite the existing file if it exists
    aggregate: TagAggregationPeriod
        The period for which the tags should be aggregated
    """
    logger.info("Starting word frequency extraction...")

    if not data_path.is_dir():
        logger.error("The provided path is not a valid directory.")
        return

    if aggregate != TagAggregationPeriod.DAILY:
        logger.error(
            "Currently, only daily aggregation is supported. Please use TagAggregationPeriod.DAILY."
        )
        return

    if save_to_file.exists() and not force_overwrite:
        logger.warning(
            f"The file {save_to_file} already exists. Use --force-overwrite to overwrite it."
        )
        return

    if force_overwrite and save_to_file.exists():
        logger.debug(f"Overwriting existing file: {save_to_file}")
        save_to_file.unlink()

    tags_by_date = aggregate_tags_by_date(data_path, TagAggregationPeriod.DAILY)

    if tags_by_date:
        with open(save_to_file, "w") as file:
            file.write(tags_by_date.model_dump_json())

    logger.debug("Word frequency extraction completed.")

    return tags_by_date
