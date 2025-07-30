# Plan zur Analyse der interessantesten Themen mittels KI-Agent

**Ziel:** Identifizierung der drei "interessantesten" Themen aus den `analysis.json` Dateien eines bestimmten Monats.

* **"Interessantes Thema"**: Ein Thema, dessen häufig vorkommende Schlüsselbegriffe (identifiziert durch ein Large Language Model - LLM) oft in den `summary`-Feldern der Dokumente des betreffenden Monats erscheinen.
* **"Themenidentifikation"**: Themen werden mittels Topic Modeling aus den Feldern `summary` und `title` extrahiert.
* **Datenquelle**: JSON-Dateien im Verzeichnis `sample-data/` und dessen Unterverzeichnissen.
* **Filterung**: Nach dem Feld `creation_date` im JSON-Inhalt.

**Vorgeschlagener Workflow:**

```mermaid
graph TD
    A[Start: Analyse der Top 3 interessantesten Themen] --> B{Phase 1: Datenerfassung & -aufbereitung};
    B --> B1[1.1: Alle 'analysis.json' Dateien im 'sample-data/' Verzeichnis rekursiv suchen];
    B1 --> B2[1.2: Dateien nach 'creation_date' im JSON-Inhalt filtern (Zielmonat)];
    B2 --> B3[1.3: 'title' und 'summary' aus gefilterten Dateien extrahieren];
    B3 --> B4[1.4: Textvorverarbeitung (z.B. Bereinigung, Normalisierung)];
    B4 --> C{Phase 2: Themenextraktion & Schlüsselwortidentifikation};
    C --> C1[2.1: Topic Modeling (z.B. BERTopic, LDA) auf vorverarbeiteten 'title' + 'summary' Texten anwenden, um Themen-Cluster zu bilden];
    C1 --> C2[2.2: LLM-basierte Schlüsselwortidentifikation];
    B3 --> C2; % Original 'summary' Texte als Input für LLM
    C1 --> C2; % Themen-Definitionen (z.B. Top-Wörter des Topics) als Kontext für LLM
    C2 --> C2a[Für jedes Dokument und dessen zugeordnete(s) Thema/Themen: LLM identifiziert relevante & häufige Schlüsselwörter im 'summary' Text, die zum Thema passen];
    C2a --> D{Phase 3: Berechnung der Themenrelevanz & Ranking};
    D --> D1[3.1: Aggregation der LLM-identifizierten Schlüsselwörter pro Thema über alle relevanten Dokumente des Monats];
    D1 --> D2[3.2: Berechnung eines 'Interesse-Scores' für jedes Thema (basierend auf der Häufigkeit der aggregierten Schlüsselwörter in den 'summary' Texten)];
    D2 --> D3[3.3: Themen nach 'Interesse-Score' absteigend sortieren];
    D3 --> E{Phase 4: Ergebnispräsentation};
    E --> E1[4.1: Ausgabe der Top 3 interessantesten Themen (inkl. repräsentativer Schlüsselwörter und ggf. kurzer Begründung)];
```

**Detaillierte Schritte des Plans:**

**Phase 1: Datenerfassung und -aufbereitung**

1. **1.1: Dateisuche:**
    * Der Agent durchsucht das Verzeichnis `sample-data/` (und alle Unterverzeichnisse) rekursiv nach Dateien mit dem Namen `analysis.json`.
    * Werkzeug: `list_files` mit rekursivem Scan.
2. **1.2: Zeitliche Filterung:**
    * Für jede gefundene `analysis.json` Datei liest der Agent den Inhalt.
    * Er extrahiert das Feld `creation_date` und prüft, ob es in den gewünschten Analysezeitraum (z.B. einen spezifischen Monat) fällt. Nur passende Dateien werden weiterverarbeitet.
    * Werkzeug: `read_file` für jede Datei, dann JSON-Parsing.
3. **1.3: Datenextraktion:**
    * Aus den gefilterten Dateien extrahiert der Agent die Inhalte der Felder `title` und `summary`.
4. **1.4: Textvorverarbeitung:**
    * Die extrahierten Texte aus `title` und `summary` werden für die weitere Analyse vorbereitet. Dies kann umfassen:
        * Umwandlung in Kleinbuchstaben.
        * Entfernung von Satzzeichen und Sonderzeichen.
        * Entfernung von Stoppwörtern (allgemeine Füllwörter).
        * Ggf. Lemmatisierung oder Stemming (Reduktion von Wörtern auf ihre Grundform). *Hinweis: Für die spätere LLM-basierte Schlüsselwortextraktion ist eine weniger aggressive Vorverarbeitung oft besser, während klassisches Topic Modeling von stärkerer Vorverarbeitung profitieren kann.*

**Phase 2: Themenextraktion und Schlüsselwortidentifikation**

1. **2.1: Topic Modeling:**
    * Auf die vorverarbeiteten (kombinierten) Texte aus `title` und `summary` wird ein Topic-Modeling-Algorithmus angewendet (z.B. LDA, NMF oder modernere Ansätze wie BERTopic, die auf Transformer-Modellen basieren).
    * Ziel ist es, eine Menge von latenten Themen zu identifizieren, die in den Dokumenten des Monats behandelt werden. Jedes Thema wird typischerweise durch eine Liste von charakteristischen Wörtern repräsentiert.
2. **2.2: LLM-basierte Schlüsselwortidentifikation:**
    * Für jedes Dokument und für jedes Thema, dem das Dokument zugeordnet wurde (durch das Topic Modeling):
        * Ein Large Language Model (LLM) analysiert den originalen `summary`-Text des Dokuments.
        * Das LLM erhält dabei den Kontext des Themas (z.B. die Top-Wörter des Themas aus Schritt 2.1 oder eine generierte Themenbezeichnung).
        * Aufgabe des LLM ist es, innerhalb des `summary`-Textes häufig vorkommende und besonders relevante Schlüsselbegriffe zu identifizieren, die spezifisch zu diesem Thema passen.
    * *Wichtiger Aspekt hierbei ist das Prompt Engineering für das LLM, um präzise und relevante Schlüsselwörter zu erhalten.*

**Phase 3: Berechnung der Themenrelevanz und Ranking**

1. **3.1: Aggregation der Schlüsselwörter:**
    * Für jedes in Schritt 2.1 identifizierte Thema werden alle vom LLM (Schritt 2.2) extrahierten Schlüsselwörter aus allen zugehörigen Dokumenten des Monats gesammelt.
2. **3.2: Berechnung des "Interesse-Scores":**
    * Für jedes Thema wird ein "Interesse-Score" berechnet. Dieser Score quantifiziert, wie "interessant" das Thema im betrachteten Monat war.
    * Der Score basiert auf der Häufigkeit der in Schritt 3.1 aggregierten, LLM-identifizierten Schlüsselwörter in den `summary`-Texten. Dies könnte eine einfache Summe der Frequenzen sein oder eine gewichtete Zählung.
3. **3.3: Themen-Ranking:**
    * Die Themen werden basierend auf ihrem "Interesse-Score" in absteigender Reihenfolge sortiert.

**Phase 4: Ergebnispräsentation**

1. **4.1: Ausgabe der Top-Themen:**
    * Die drei Themen mit den höchsten Interesse-Scores werden als Ergebnis präsentiert.
    * Zusätzlich sollten die wichtigsten LLM-identifizierten Schlüsselwörter für jedes dieser Top-Themen angezeigt werden, um die Ergebnisse nachvollziehbar zu machen. Ggf. können auch repräsentative Textausschnitte aus den `summary`-Feldern als Beispiele dienen.
