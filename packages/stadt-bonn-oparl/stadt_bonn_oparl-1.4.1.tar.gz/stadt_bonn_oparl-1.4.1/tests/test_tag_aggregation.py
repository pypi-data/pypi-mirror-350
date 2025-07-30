import json
import shutil
import tempfile
from pathlib import Path

import pytest

from stadt_bonn.oparl.papers.models import TagAggregationPeriod
from stadt_bonn.oparl.papers.tag_aggregation import aggregate_tags_by_date


@pytest.fixture
def temp_analysis_dir():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


def write_analysis_json(path, creation_date, tags):
    data = {
        "creation_date": creation_date,
        "tags": tags,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def test_aggregate_tags_by_date_single_file(temp_analysis_dir):
    analysis_file = temp_analysis_dir / "analysis.json"
    write_analysis_json(analysis_file, "2024-06-01", ["foo", "bar", "foo"])
    result = aggregate_tags_by_date(temp_analysis_dir, TagAggregationPeriod.DAILY)
    assert "2024-06-01" in result.data
    tag_counts = {tc.tag: tc.count for tc in result.data["2024-06-01"]}
    assert tag_counts["foo"] == 2
    assert tag_counts["bar"] == 1


def test_aggregate_tags_by_date_multiple_files(temp_analysis_dir):
    (temp_analysis_dir / "a").mkdir()
    (temp_analysis_dir / "b").mkdir()
    write_analysis_json(
        temp_analysis_dir / "a" / "analysis.json", "2024-06-02", ["alpha"]
    )
    write_analysis_json(
        temp_analysis_dir / "b" / "analysis.json", "2024-06-02", ["beta", "alpha"]
    )
    result = aggregate_tags_by_date(temp_analysis_dir, TagAggregationPeriod.DAILY)
    assert "2024-06-02" in result.data
    tag_counts = {tc.tag: tc.count for tc in result.data["2024-06-02"]}
    assert tag_counts["alpha"] == 2
    assert tag_counts["beta"] == 1


def test_aggregate_tags_by_date_different_dates(temp_analysis_dir):
    # Create subdirectory for the first date
    date1_dir = temp_analysis_dir / "date1"
    date1_dir.mkdir()
    write_analysis_json(date1_dir / "analysis.json", "2024-06-03", ["x"])

    # Create subdirectory for the second date
    date2_dir = temp_analysis_dir / "date2"
    date2_dir.mkdir()
    write_analysis_json(date2_dir / "analysis.json", "2024-06-04", ["y", "x"])
    result = aggregate_tags_by_date(temp_analysis_dir, TagAggregationPeriod.DAILY)
    assert "2024-06-03" in result.data
    assert "2024-06-04" in result.data
    tag_counts_1 = {tc.tag: tc.count for tc in result.data["2024-06-03"]}
    tag_counts_2 = {tc.tag: tc.count for tc in result.data["2024-06-04"]}
    assert tag_counts_1["x"] == 1
    assert tag_counts_2["y"] == 1
    assert tag_counts_2["x"] == 1


def test_aggregate_tags_by_date_empty_tags(temp_analysis_dir):
    write_analysis_json(temp_analysis_dir / "analysis.json", "2024-06-05", [])
    result = aggregate_tags_by_date(temp_analysis_dir, TagAggregationPeriod.DAILY)
    assert "2024-06-05" not in result.data or result.data["2024-06-05"] == []
