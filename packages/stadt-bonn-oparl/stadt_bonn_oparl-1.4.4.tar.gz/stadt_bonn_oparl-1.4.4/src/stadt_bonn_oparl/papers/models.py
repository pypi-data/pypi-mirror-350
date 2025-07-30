from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Paper(BaseModel):
    """
    A class representing a paper with its content and metadata. Bassed on https://schema.oparl.org/1.1/Paper
    """

    id: str  # ID of the paper
    metadata: dict  # metadata has been returned by the OPARL API
    content: str  # this is markdown extracted from the PDF using docling


class UnifiedPaper(BaseModel):
    paper_id: str
    metadata: Dict[str, Any]
    analysis: Dict[str, Any]
    markdown_text: str
    external_oparl_data: Dict[str, Optional[Dict[str, Any]]]
    enrichment_status: str
    # validation_status will be added in the next step
    # validation_errors: List[str]


class PaperType(str, Enum):
    """Enum representing the type of paper. Based on https://oparl.org/spezifikation/online-ansicht/#entity-paper"""

    unbekannt = "Unbekannt"
    buerger_antrag = "Anregungen und Beschwerden"
    antrag = "Antrag"
    beschlussvorlage = "Beschlussvorlage"
    informationsbrief = "Informationsbrief"
    mitteilungsvorlage = "Mitteilungsvorlage"
    stellungnahme_der_verwaltung = "Stellungnahme der Verwaltung"


class PaperAnalysis(BaseModel):
    id: str
    title: str
    type: PaperType
    creation_date: str
    responsible_department: str
    decision_body: Optional[str]
    decision_date: Optional[str]
    subject_area: str
    geographic_scope: str
    priority_level: str
    main_proposal: str
    key_stakeholders: List[str]
    summary: str
    tags: List[str]
    next_steps: Optional[str]
    additional_notes: Optional[str]


# Enum for the Tag aggregation period
class TagAggregationPeriod(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class TagCount(BaseModel):
    tag: str
    count: int

    def __add__(self, other: Any) -> "TagCount":
        if not isinstance(other, (TagCount, int)):
            return NotImplemented
        if isinstance(other, int):
            return TagCount(tag=self.tag, count=self.count + other)
        if self.tag != other.tag:
            raise ValueError("Cannot add TagCounts with different tags")
        return TagCount(tag=self.tag, count=self.count + other.count)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TagCount):
            return NotImplemented
        return self.tag == other.tag and self.count == other.count

    def __hash__(self) -> int:
        return hash((self.tag, self.count))

    def __repr__(self) -> str:
        return f"TagCount(tag={self.tag!r}, count={self.count})"

    def __str__(self) -> str:
        return f"{self.tag}: {self.count}"


class TagAggregation(BaseModel):
    period: TagAggregationPeriod
    data: Dict[str, List[TagCount]]

    def add_tag_count(self, date: str, tag_count: TagCount) -> None:
        if date not in self.data:
            self.data[date] = []
        for existing_tag_count in self.data[date]:
            if existing_tag_count.tag == tag_count.tag:
                existing_tag_count.count += tag_count.count
                return
        self.data[date].append(tag_count)
