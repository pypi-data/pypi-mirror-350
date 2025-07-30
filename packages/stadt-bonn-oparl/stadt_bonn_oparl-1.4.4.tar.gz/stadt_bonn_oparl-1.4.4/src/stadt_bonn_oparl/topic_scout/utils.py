from datetime import datetime
from typing import Any, Dict, List

from stadt_bonn_oparl.topic_scout.models import (
    DataSource,
    Document,
    DocumentStatus,
    DocumentType,
)


def create_document_from_search_result(search_data: Dict[str, Any]) -> Document:
    """Erstellt ein Document-Objekt aus Suchergebnissen"""
    return Document(
        drucksachen_nummer=search_data.get("drucksachen_nummer", ""),
        titel=search_data.get("titel", ""),
        erstellungsdatum=search_data.get("erstellungsdatum", datetime.now()),
        letzte_aenderung=search_data.get("letzte_aenderung"),
        status=(
            DocumentStatus(search_data["status"]) if search_data.get("status") else None
        ),
        dokumenttyp=(
            DocumentType(search_data["dokumenttyp"])
            if search_data.get("dokumenttyp")
            else None
        ),
        zustaendige_gremien=search_data.get("zustaendige_gremien", []),
        verantwortliche_abteilung=search_data.get("verantwortliche_abteilung"),
        relevanz_score=search_data.get("relevanz_score"),
        kurzbeschreibung=search_data.get("kurzbeschreibung"),
        tags=search_data.get("tags", []),
        datenquelle=DataSource(
            search_data.get("datenquelle", DataSource.CHROMADB.value)
        ),
    )


def merge_results_from_sources(
    chromadb_results: List[Dict], mcp_metadata: List[Dict]
) -> List[Document]:
    """Kombiniert Ergebnisse aus ChromaDB und MCP-Tools"""
    documents = []

    # Erstelle ein Mapping von Drucksachennummern zu MCP-Metadaten
    mcp_lookup = {meta["drucksachen_nummer"]: meta for meta in mcp_metadata}

    for result in chromadb_results:
        # Basis-Dokument aus ChromaDB erstellen
        doc_data = result.copy()

        # MCP-Metadaten hinzufügen, falls vorhanden
        drucksachen_nr = result.get("drucksachen_nummer")
        if drucksachen_nr in mcp_lookup:
            mcp_data = mcp_lookup[drucksachen_nr]
            doc_data.update(mcp_data)
            doc_data["datenquelle"] = DataSource.COMBINED.value

        documents.append(create_document_from_search_result(doc_data))

    return documents
