# Stadt Bonn Ratsinfo

Dieses Projekt enthält Tools zur Verarbeitung von Ratsinformationen der Stadt Bonn.

## Beschreibung

...

## Installation

### Install `uv`

The first thing to do is make sure `uv` is installed, as `uv` is used in this project.

For installation instructions, see the [`uv` installation docs](https://docs.astral.sh/uv/getting-started/installation/).

If you already have an older version of `uv` installed, you might need to update it with `uv self update`.

```bash
uv install
```

## Nutzung

`uv run oparl download paper --data-path data/ --max-pages 1`

und `uv run oparl convert paper --data-path data/ --all`

```bash
uv run oparl classify \
 --data-path data/2025-05-19_253130-02_Bürgerantrag_Stopp_des_Bauvorhabens_Nr._7213-2_Schloßallee/2025-05-16_253130-02_Buergerantrag_Stopp_SAO.md
```

### MCP Server starten

```bash
uv run fastmcp run src/stadt_bonn/oparl/mcp/server.py --transport sse
```

### Topic Scout testen

`uv run scripts/test_topic_scout.py`

## Datenexploration

Im Notebook [explore analysis](./notebooks/explore_analysis.ipynb) finden Sie eine erste Analyse der Daten. Hier werden
verschiedene Aspekte der Daten untersucht, um ein besseres Verständnis für die Struktur und den Inhalt der
Ratsinformationen zu gewinnen.

## Rechtliches

Die Daten stammen von der Stadt Bonn und unterliegen den jeweiligen Lizenzbedingungen. Bitte beachten Sie die Lizenzbedingungen, bevor Sie die Daten verwenden oder weitergeben. Die Dateien in diesem Repository unterliegen der GPL-3.0-Lizenz. Weitere Informationen finden Sie in der Datei `LICENSE`.
