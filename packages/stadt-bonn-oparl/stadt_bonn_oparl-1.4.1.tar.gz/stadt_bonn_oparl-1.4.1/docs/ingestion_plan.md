# OParl Data Ingestion Plan for RAG Agent

This document outlines the plan for ingesting OParl data (from `metadata.json`, `analysis.json`, and markdown content files) into a Vector Database to be used by a RAG (Retrieval Augmented Generation) agent.

## Goal

To create a robust and flexible ingestion pipeline that:

1. Acquires data from local JSON and Markdown files.
2. Enriches this data by fetching related information from OParl API URLs.
3. Consolidates and validates the data.
4. Prepares and chunks textual content for vector embedding.
5. Generates vector embeddings.
6. Packages the data (text, embeddings, rich metadata) for ingestion into a Vector Database.

## Key Considerations from User Feedback

* The specific Vector Database is yet to be decided. The plan should be flexible.
* The RAG agent will primarily be used for summarizing documents and finding related papers.
* When fetching data from external OParl URLs, all available fields should be captured.
* If an external URL fetch fails, the ingestion for that paper should be marked as "incomplete_external_data", and the process should continue for that paper.
* A data validation step is crucial after data consolidation.

## Data Ingestion Plan Phases

**Phase 1: Data Acquisition and Initial Processing**

1. **Input:** A directory for each political paper containing:
    * `metadata.json` (e.g., [`sample-data/2025-04-25_252775-02_N-Vorlage_zum_CDU-Antrag_Priorisierungsliste_Instandsetzung_Baudenkmäler/metadata.json`](sample-data/2025-04-25_252775-02_N-Vorlage_zum_CDU-Antrag_Priorisierungsliste_Instandsetzung_Baudenkmäler/metadata.json))
    * `analysis.json` (e.g., [`sample-data/2025-04-25_252775-02_N-Vorlage_zum_CDU-Antrag_Priorisierungsliste_Instandsetzung_Baudenkmäler/analysis.json`](sample-data/2025-04-25_252775-02_N-Vorlage_zum_CDU-Antrag_Priorisierungsliste_Instandsetzung_Baudenkmäler/analysis.json))
    * The corresponding markdown content file (e.g., [`sample-data/2025-04-25_252775-02_N-Vorlage_zum_CDU-Antrag_Priorisierungsliste_Instandsetzung_Baudenkmäler/2025-04-11_252775-02_N-Vorlage_zum_CDU-An_SAO.md`](sample-data/2025-04-25_252775-02_N-Vorlage_zum_CDU-Antrag_Priorisierungsliste_Instandsetzung_Baudenkmäler/2025-04-11_252775-02_N-Vorlage_zum_CDU-An_SAO.md))
2. **Core File Loading:**
    * Parse `metadata.json` to extract base attributes and all URLs for enrichment.
    * Parse `analysis.json` for its summarized content and structured analytical data.
    * Load the full text from the `.md` file.
3. **External Data Enrichment & Status Tracking:**
    * For each URL identified in `metadata.json` (e.g., `originatorPerson`, `underDirectionOf`, `consultation.organization`, `consultation.meeting`):
        * Attempt to fetch data from the URL (expecting JSON responses).
        * Capture *all available fields* from the JSON response.
        * If a fetch fails (timeout, network error, non-2xx response), log the error and the specific URL.
    * Maintain an `ingestion_status` for the paper (e.g., "complete", "incomplete_external_data"). If any external fetch fails, this status will be marked accordingly.

**Phase 2: Data Consolidation, Validation, and Structuring for RAG**

1. **Unified Paper Object Creation:** For each paper, create a comprehensive in-memory object (e.g., a Python dictionary or a custom class instance). This object will aggregate:
    * All data from `metadata.json`.
    * All data from `analysis.json`.
    * The full text from the `.md` file.
    * All successfully fetched and parsed data from external OParl entities, nested appropriately.
    * The `ingestion_status`.
2. **Data Validation:**
    * After creating the Unified Paper Object, perform validation checks.
    * **Checks could include:**
        * Presence of mandatory fields (e.g., a paper ID/reference, main textual content from the `.md` file).
        * Basic data type checks for critical fields (e.g., `date` fields are in a recognizable date format).
        * Verification that the `ingestion_status` accurately reflects any fetching issues.
    * **Outcome:** If validation fails critical checks, the paper might be flagged for review, or processing for that paper might halt, depending on the severity. Log all validation errors. A `validation_status` (e.g., "passed", "failed_critical", "passed_with_warnings") should be added to the paper's metadata.
3. **Text Compilation & Chunking Strategy (Post-Validation):**
    * If validation passes (or passes with warnings, depending on policy), proceed to compile key textual components:
        * The full content of the `.md` file.
        * The `summary` and potentially other relevant text fields from `analysis.json`.
        * Key textual information from enriched entities (e.g., names of persons/organizations, meeting topics/summaries if available).
    * **Chunking:** Divide the compiled text into manageable, semantically coherent chunks. The chunk size will need to be optimized based on the chosen embedding model's context window and the nature of the RAG queries.
    * **Metadata per Chunk:** Each chunk must be associated with rich metadata derived from the (now validated) Unified Paper Object. This includes, but is not limited to:
        * `paper_id` (e.g., `metadata.reference` or `metadata.id`)
        * `paper_name` (e.g., `metadata.name`)
        * `paper_date` (e.g., `metadata.date`)
        * `paper_web_url` (e.g., `metadata.web`)
        * `source_document_filename` (e.g., the name of the `.md` file)
        * `analysis_tags` (from `analysis.json`)
        * `analysis_key_stakeholders` (from `analysis.json`)
        * `involved_person_ids_and_names` (list of dicts: `{'id': 'url', 'name': 'fetched_name'}`)
        * `involved_organization_ids_and_names` (list of dicts)
        * `consultation_meeting_ids_and_dates` (list of dicts)
        * `paper_ingestion_status`
        * `paper_validation_status`

**Phase 3: Vectorization and Preparation for Storage**

1. **Embedding Generation:** For each text chunk that comes from a paper that passed validation, generate a vector embedding using a suitable sentence transformer or language model.
2. **Data Packaging for Vector DB:** Prepare a list of objects, where each object represents a chunk and contains:
    * The original `chunk_text`.
    * Its `vector_embedding`.
    * All the `metadata` detailed in Phase 2 (Chunking Strategy).
    This list of objects is what will eventually be loaded into the chosen Vector Database.

## Workflow Diagram

```mermaid
graph TD
    A[Start: Paper Directory] --> B{Load Core Files};
    B -- metadata.json --> C[Parse Metadata];
    B -- analysis.json --> D[Parse Analysis];
    B -- *.md --> E[Load Full Text];

    C --> F{Extract URLs for Enrichment};
    F -- Person URLs --> G[Fetch All Person Data];
    F -- Org URLs --> H[Fetch All Organization Data];
    F -- Meeting URLs --> I[Fetch All Meeting Data];
    F -- Other Linked URLs --> J[Fetch All Other Linked Data];

    subgraph EnrichmentModule
        direction LR
        G -.-> S_FetchStatus;
        H -.-> S_FetchStatus;
        I -.-> S_FetchStatus;
        J -.-> S_FetchStatus;
    end

    S_FetchStatus{Track Fetch Status per URL} --> K_Status[Update Paper Ingestion Status];

    K_Consolidate[Consolidate All Data into Unified Paper Object]
    C --> K_Consolidate;
    D --> K_Consolidate;
    E --> K_Consolidate;
    G -- Enriched Data --> K_Consolidate;
    H -- Enriched Data --> K_Consolidate;
    I -- Enriched Data --> K_Consolidate;
    J -- Enriched Data --> K_Consolidate;
    K_Status -- ingestion_status --> K_Consolidate;

    K_Consolidate --> V[Validate Unified Paper Object];
    V -- Validated Data --> L[Compile & Preprocess Text for RAG];
    V -- Validation Issues --> Log_Review[Log Issues / Flag for Review / Update Validation Status];

    L --> M[Strategic Text Chunking with Rich Metadata];
    M --> N[Generate Vector Embeddings for Chunks];
    N --> O[Package Chunks, Embeddings & Metadata];
    O --> P[End: Data Ready for Vector DB Ingestion];
