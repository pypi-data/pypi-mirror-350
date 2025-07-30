from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class DocumentStatus(Enum):
    """Status eines Dokuments im politischen Prozess"""

    ENTWURF = "Entwurf"
    EINGEREICHT = "Eingereicht"
    IN_BEARBEITUNG = "In Bearbeitung"
    BESCHLOSSEN = "Beschlossen"
    ABGELEHNT = "Abgelehnt"
    ZURÜCKGESTELLT = "Zurückgestellt"
    ERLEDIGT = "Erledigt"


class DocumentType(Enum):
    """Typ des Dokuments"""

    BESCHLUSSVORLAGE = "Beschlussvorlage"
    BUERGERANTRAG = "Bürgerantrag"
    MITTEILUNGSVORLAGE = "Mitteilungsvorlage"
    ANFRAGE = "Anfrage"
    ANTRAG = "Antrag"
    STELLUNGNAHME = "Stellungnahme"
    BERICHT = "Bericht"


class DataSource(Enum):
    """Quelle der Daten"""

    CHROMADB = "ChromaDB Vektordatenbank"
    MCP_TOOLS = "MCP-Tools Metadaten"
    COMBINED = "Kombinierte Quellen"


@dataclass
class Document(BaseModel):
    """Repräsentiert ein einzelnes Dokument mit allen verfügbaren Informationen"""

    drucksachen_nummer: str
    titel: str
    erstellungsdatum: datetime
    letzte_aenderung: Optional[datetime] = None
    status: Optional[DocumentStatus] = None
    dokumenttyp: Optional[DocumentType] = None
    zustaendige_gremien: List[str] = field(default_factory=list)
    verantwortliche_abteilung: Optional[str] = None
    relevanz_score: Optional[float] = None
    kurzbeschreibung: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    datenquelle: DataSource = DataSource.CHROMADB

    def __post_init__(self):
        """Validierung und Normalisierung nach Initialisierung"""
        if isinstance(self.erstellungsdatum, str):
            self.erstellungsdatum = datetime.fromisoformat(self.erstellungsdatum)
        if isinstance(self.letzte_aenderung, str):
            self.letzte_aenderung = datetime.fromisoformat(self.letzte_aenderung)


@dataclass
class DocumentLink(BaseModel):
    """Repräsentiert eine Verknüpfung zwischen Dokumenten"""

    ziel_drucksache: str
    beziehungstyp: str  # z.B. "Folgedokument", "Ergänzung", "Bezug"
    beschreibung: Optional[str] = None


@dataclass
class Stakeholder(BaseModel):
    """Repräsentiert einen beteiligten Akteur"""

    name: str
    typ: str  # z.B. "Gremium", "Abteilung", "Ausschuss"
    rolle: Optional[str] = None  # z.B. "Federführend", "Beratend"
    anzahl_dokumente: int = 0


@dataclass
class ThematicCategory(BaseModel):
    """Repräsentiert eine thematische Unterkategorie"""

    name: str
    beschreibung: Optional[str] = None
    dokumente: List[Document] = field(default_factory=list)
    unterkategorien: List["ThematicCategory"] = field(default_factory=list)

    @property
    def anzahl_dokumente_gesamt(self) -> int:
        """Gesamtanzahl Dokumente inklusive Unterkategorien"""
        gesamt = len(self.dokumente)
        for unterkategorie in self.unterkategorien:
            gesamt += unterkategorie.anzahl_dokumente_gesamt
        return gesamt


@dataclass
class TrendAnalysis(BaseModel):
    """Repräsentiert eine Trend- oder Zeitreihenanalyse"""

    zeitraum_start: datetime
    zeitraum_ende: datetime
    anzahl_dokumente: int
    wichtige_entwicklungen: List[str] = field(default_factory=list)
    haeufigste_dokumenttypen: Dict[DocumentType, int] = field(default_factory=dict)
    aktivste_gremien: Dict[str, int] = field(default_factory=dict)


@dataclass
class TopicScoutResult(BaseModel):
    """Hauptklasse für die Ergebnisse einer TopicScout-Analyse"""

    # Basis-Informationen
    thema: str
    analysezeitpunkt: datetime = field(default_factory=datetime.now)

    # Themenübersicht
    themen_beschreibung: str = ""
    relevanz_einschaetzung: str = ""
    umfang_bewertung: str = ""

    # Hauptkategorien und Dokumente
    hauptkategorien: List[ThematicCategory] = field(default_factory=list)
    alle_dokumente: List[Document] = field(default_factory=list)

    # Stakeholder-Informationen
    stakeholder: List[Stakeholder] = field(default_factory=list)

    # Trends und Entwicklungen
    trends: List[TrendAnalysis] = field(default_factory=list)
    zeitliche_entwicklung: str = ""

    # Verknüpfungen
    dokumentverknuepfungen: Dict[str, List[DocumentLink]] = field(default_factory=dict)

    # Metadaten und Datenquellen
    genutzte_datenquellen: List[DataSource] = field(default_factory=list)
    qualitaetsbewertung: Optional[str] = None
    limitierungen: List[str] = field(default_factory=list)

    # Suchparameter
    suchparameter: Dict[str, Any] = field(default_factory=dict)

    def add_document(self, document: Document, kategorie_name: Optional[str] = None):
        """Fügt ein Dokument hinzu und ordnet es optional einer Kategorie zu"""
        self.alle_dokumente.append(document)

        if kategorie_name:
            kategorie = self.get_or_create_category(kategorie_name)
            kategorie.dokumente.append(document)

    def get_or_create_category(self, name: str) -> ThematicCategory:
        """Findet eine Kategorie oder erstellt eine neue"""
        for kategorie in self.hauptkategorien:
            if kategorie.name == name:
                return kategorie

        neue_kategorie = ThematicCategory(name=name)
        self.hauptkategorien.append(neue_kategorie)
        return neue_kategorie

    def add_stakeholder(self, name: str, typ: str, rolle: Optional[str] = None):
        """Fügt einen Stakeholder hinzu oder aktualisiert die Dokumentanzahl"""
        for stakeholder in self.stakeholder:
            if stakeholder.name == name and stakeholder.typ == typ:
                stakeholder.anzahl_dokumente += 1
                return stakeholder

        neuer_stakeholder = Stakeholder(
            name=name, typ=typ, rolle=rolle, anzahl_dokumente=1
        )
        self.stakeholder.append(neuer_stakeholder)
        return neuer_stakeholder

    def add_document_link(
        self,
        von_drucksache: str,
        zu_drucksache: str,
        beziehungstyp: str,
        beschreibung: Optional[str] = None,
    ):
        """Fügt eine Dokumentverknüpfung hinzu"""
        if von_drucksache not in self.dokumentverknuepfungen:
            self.dokumentverknuepfungen[von_drucksache] = []

        link = DocumentLink(
            ziel_drucksache=zu_drucksache,
            beziehungstyp=beziehungstyp,
            beschreibung=beschreibung,
        )
        self.dokumentverknuepfungen[von_drucksache].append(link)

    @property
    def gesamtanzahl_dokumente(self) -> int:
        """Gesamtanzahl aller gefundenen Dokumente"""
        return len(self.alle_dokumente)

    @property
    def aktuelle_dokumente(self) -> List[Document]:
        """Dokumente aus dem letzten Jahr"""
        ein_jahr_zurueck = datetime.now().replace(year=datetime.now().year - 1)
        return [
            doc
            for doc in self.alle_dokumente
            if doc.erstellungsdatum >= ein_jahr_zurueck
        ]

    @property
    def haeufigste_gremien(self) -> Dict[str, int]:
        """Die am häufigsten beteiligten Gremien"""
        gremien_count = {}
        for doc in self.alle_dokumente:
            for gremium in doc.zustaendige_gremien:
                gremien_count[gremium] = gremien_count.get(gremium, 0) + 1
        return dict(sorted(gremien_count.items(), key=lambda x: x[1], reverse=True))

    def to_summary_dict(self) -> Dict[str, Any]:
        """Erstellt eine Zusammenfassung als Dictionary für einfache Serialisierung"""
        return {
            "thema": self.thema,
            "analysezeitpunkt": self.analysezeitpunkt.isoformat(),
            "gesamtanzahl_dokumente": self.gesamtanzahl_dokumente,
            "anzahl_kategorien": len(self.hauptkategorien),
            "anzahl_stakeholder": len(self.stakeholder),
            "haeufigste_gremien": dict(list(self.haeufigste_gremien.items())[:5]),
            "aktuelle_dokumente_anzahl": len(self.aktuelle_dokumente),
            "genutzte_datenquellen": [ds.value for ds in self.genutzte_datenquellen],
            "qualitaetsbewertung": self.qualitaetsbewertung,
        }
