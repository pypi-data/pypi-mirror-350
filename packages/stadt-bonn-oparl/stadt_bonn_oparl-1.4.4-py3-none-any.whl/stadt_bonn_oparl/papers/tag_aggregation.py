import json
from pathlib import Path

from stadt_bonn_oparl.papers.models import (
    TagAggregation,
    TagAggregationPeriod,
    TagCount,
)


def aggregate_tags_by_date(
    data_path: Path, aggregate: TagAggregationPeriod
) -> TagAggregation:
    """
    Aggregate tags from OPARL Papers analysis files by their creation date.

    for the creation_date, we add a dict with the tag and the count
    if the creation_date is already in the list, we add the tag to the existing dict
    and if the tag is already in the dict, we add the count to the existing count

    Parameters
    ----------
    data_path: str
        Path to the directory containing OPARL Papers analysis files.

    Returns
    -------
    TagAggregation
        An object containing the aggregated tags by date.
    """
    tags_by_date: TagAggregation = TagAggregation(period=aggregate, data={})

    # Process each analysis file in the directory
    for analysis_file in data_path.glob("**/analysis.json"):
        # extract the creation_data and tags
        with open(analysis_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            creation_date = data.get("creation_date")
            tags = data.get("tags", [])

            # for the creation_date, we add a dict with the tag and the count
            # if the creation_date is already in the list, we add the tag to the existing dict
            # and if the tag is already in the dict, we add the count to the existing count
            for tag in tags:
                tags_by_date.add_tag_count(creation_date, TagCount(tag=tag, count=1))

    return tags_by_date
