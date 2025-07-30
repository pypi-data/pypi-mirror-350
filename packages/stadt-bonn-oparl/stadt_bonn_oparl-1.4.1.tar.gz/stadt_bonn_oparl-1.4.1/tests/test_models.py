import pytest

from stadt_bonn.oparl.papers.models import (
    TagCount,
    TagAggregation,
    TagAggregationPeriod,
    PaperType,
    PaperAnalysis,
    Paper,
    UnifiedPaper,
)


def test_tagcount_addition():
    t1 = TagCount(tag="foo", count=2)
    t2 = TagCount(tag="foo", count=3)
    result = t1 + t2
    assert isinstance(result, TagCount)
    assert result.tag == "foo"
    assert result.count == 5


def test_tagcount_addition_different_tags_raises():
    t1 = TagCount(tag="foo", count=2)
    t2 = TagCount(tag="bar", count=3)
    with pytest.raises(ValueError):
        _ = t1 + t2


def test_tagcount_equality_and_hash():
    t1 = TagCount(tag="foo", count=2)
    t2 = TagCount(tag="foo", count=2)
    t3 = TagCount(tag="foo", count=3)
    assert t1 == t2
    assert t1 != t3
    assert hash(t1) == hash(t2)
    assert hash(t1) != hash(t3)


def test_tagcount_repr_and_str():
    t = TagCount(tag="foo", count=7)
    assert repr(t) == "TagCount(tag='foo', count=7)"
    assert str(t) == "foo: 7"


def test_tagaggregation_model():
    tag_counts = [TagCount(tag="foo", count=1), TagCount(tag="bar", count=2)]
    agg = TagAggregation(
        period=TagAggregationPeriod.DAILY, data={"2024-01-01": tag_counts}
    )
    assert agg.period == TagAggregationPeriod.DAILY
    assert agg.data["2024-01-01"] == tag_counts


def test_papertype_enum():
    assert PaperType.antrag.value == "Antrag"
    assert PaperType["antrag"] == PaperType.antrag


def test_paperanalysis_model():
    analysis = PaperAnalysis(
        id="1",
        title="Test Paper",
        type=PaperType.antrag,
        creation_date="2024-01-01",
        responsible_department="Dept",
        decision_body=None,
        decision_date=None,
        subject_area="Area",
        geographic_scope="Scope",
        priority_level="High",
        main_proposal="Proposal",
        key_stakeholders=["Stakeholder1"],
        summary="Summary",
        tags=["tag1", "tag2"],
        next_steps=None,
        additional_notes=None,
    )
    assert analysis.id == "1"
    assert analysis.type == PaperType.antrag
    assert "tag1" in analysis.tags


def test_paper_model():
    paper = Paper(id="paper-1", metadata={"foo": "bar"}, content="Some markdown")
    assert paper.id == "paper-1"
    assert paper.metadata["foo"] == "bar"
    assert paper.content == "Some markdown"


def test_unifiedpaper_model():
    up = UnifiedPaper(
        paper_id="p1",
        metadata={"foo": "bar"},
        analysis={"summary": "test"},
        markdown_text="text",
        external_oparl_data={"key": None},
        enrichment_status="done",
    )
    assert up.paper_id == "p1"
    assert up.metadata["foo"] == "bar"
    assert up.analysis["summary"] == "test"
    assert up.markdown_text == "text"
    assert up.external_oparl_data["key"] is None
    assert up.enrichment_status == "done"


def test_tagaggregationperiod_enum():
    assert TagAggregationPeriod.DAILY.value == "daily"
    assert TagAggregationPeriod["WEEKLY"] == TagAggregationPeriod.WEEKLY


def test_tagcount_add_tagcount_same_tag():
    t1 = TagCount(tag="foo", count=2)
    t2 = TagCount(tag="foo", count=5)
    result = t1 + t2
    assert isinstance(result, TagCount)
    assert result.tag == "foo"
    assert result.count == 7


def test_tagcount_add_tagcount_different_tag_raises():
    t1 = TagCount(tag="foo", count=2)
    t2 = TagCount(tag="bar", count=3)
    with pytest.raises(ValueError):
        _ = t1 + t2


def test_tagcount_add_int():
    t = TagCount(tag="foo", count=4)
    result = t + 3
    assert isinstance(result, TagCount)
    assert result.tag == "foo"
    assert result.count == 7


def test_tagcount_add_invalid_type_returns_notimplemented():
    t = TagCount(tag="foo", count=1)

    class Dummy:
        pass

    dummy = Dummy()
    result = t.__add__(dummy)
    assert result is NotImplemented


def test_add_tag_count_new_date():
    agg = TagAggregation(period=TagAggregationPeriod.DAILY, data={})
    tag_count = TagCount(tag="foo", count=2)
    agg.add_tag_count("2024-01-01", tag_count)
    assert "2024-01-01" in agg.data
    assert agg.data["2024-01-01"][0] == tag_count


def test_add_tag_count_existing_date_new_tag():
    agg = TagAggregation(
        period=TagAggregationPeriod.DAILY,
        data={"2024-01-01": [TagCount(tag="foo", count=2)]},
    )
    new_tag_count = TagCount(tag="bar", count=3)
    agg.add_tag_count("2024-01-01", new_tag_count)
    tags = {tc.tag for tc in agg.data["2024-01-01"]}
    assert "foo" in tags and "bar" in tags
    assert any(tc.tag == "bar" and tc.count == 3 for tc in agg.data["2024-01-01"])


def test_add_tag_count_existing_date_existing_tag():
    agg = TagAggregation(
        period=TagAggregationPeriod.DAILY,
        data={"2024-01-01": [TagCount(tag="foo", count=2)]},
    )
    agg.add_tag_count("2024-01-01", TagCount(tag="foo", count=5))
    assert len(agg.data["2024-01-01"]) == 1
    assert agg.data["2024-01-01"][0].tag == "foo"
    assert agg.data["2024-01-01"][0].count == 7


def test_add_tag_count_multiple_dates_and_tags():
    agg = TagAggregation(period=TagAggregationPeriod.DAILY, data={})
    agg.add_tag_count("2024-01-01", TagCount(tag="foo", count=1))
    agg.add_tag_count("2024-01-02", TagCount(tag="bar", count=2))
    agg.add_tag_count("2024-01-01", TagCount(tag="bar", count=3))
    assert set(agg.data.keys()) == {"2024-01-01", "2024-01-02"}
    tags_0101 = {tc.tag for tc in agg.data["2024-01-01"]}
    tags_0102 = {tc.tag for tc in agg.data["2024-01-02"]}
    assert tags_0101 == {"foo", "bar"}
    assert tags_0102 == {"bar"}
