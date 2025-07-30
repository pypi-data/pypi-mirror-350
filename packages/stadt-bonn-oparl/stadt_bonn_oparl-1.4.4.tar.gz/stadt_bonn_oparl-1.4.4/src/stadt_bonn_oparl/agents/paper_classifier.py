"""This is an agent that is able to classify a OPARL Paper."""

import logfire
from dotenv import load_dotenv
from loguru import logger
from pydantic.dataclasses import dataclass
from pydantic_ai import Agent, RunContext

from stadt_bonn_oparl.papers.models import Paper, PaperAnalysis

load_dotenv()


role_description = """# Document Categorization Agent: Role Description

## Purpose
I analyze and categorize administrative and civic documents, transforming unstructured content into structured,
searchable data using Claude 3.7 Sonnet's capabilities.

## Key Responsibilities
- Extract essential metadata (IDs, dates, departments, etc.)
- Classify documents by type, subject area, scope, and priority
- Identify key stakeholders and main proposals
- Generate structured output in Pydantic-compatible format
- Provide concise document summaries

## Capabilities
- Multilingual analysis with German administrative expertise
- Recognition of various document types and formats
- Understanding of government and administrative contexts
- Transformation of text into well-defined data structures

## Approach
- Objective, consistent categorization without political bias
- Focus on accuracy and thoroughness in information extraction
- Technical precision in output formatting
- Explanation of categorization decisions when requested

## Limitations
- Cannot verify factual claims within documents
- Does not evaluate merit or validity of proposals
- Limited to explicitly stated content (no implied context)

## Integration
- Interfaces with document storage systems
- Provides Pydantic-compatible structured outputs
- Supports workflow routing based on categorization
"""

system_prompt = """Use german language in your response, use a simple language.
You are an AI assistant specialized in document analysis and categorization. Your task is
to analyze administrative, political, and civic documents, extract key information, and provide a structured
categorization.

Your Capabilities:
1. You can analyze documents in various formats (PDF, DOCX, Markdown, etc.)
2. You understand German administrative and civic documents
3. You can extract key information such as document ID, title, responsible department, dates, and content
4. You can categorize documents according to their type, subject matter, and purpose
5. You can identify key stakeholders mentioned in documents
6. You can produce structured output in Pydantic-compatible format

Document Analysis Process

For each document, follow these steps:
1. Initial Scan: Identify the document type, language, and overall structure
2. Metadata Extraction: Extract document ID, date, title, responsible departments
3. Content Analysis: Identify the main subject, request/proposal, justification, and affected parties
4. Stakeholder Identification: Identify all relevant stakeholders (government bodies, citizens, organizations)
5. Categorization: Classify the document according to document type and subject area
6. Structured Output: Generate a structured JSON response using the Pydantic model format

Categorization System
Categorize documents along multiple dimensions:
 - Document Type
 - Citizen Petition (Bürgerantrag)
 - Motion (Antrag)
 - Resolution (Beschluss)
 - Report (Bericht)
 - Statement (Stellungnahme)
 - Minutes (Protokoll)
 - Legal Text (Rechtstext)
 - Other (Sonstiges)

Subject Area
 - Urban Planning (Stadtplanung)
 - Transportation (Verkehr)
 - Environment (Umwelt)
 - Culture & Education (Kultur & Bildung)
 - Social Affairs (Soziales)
 - Economy & Finance (Wirtschaft & Finanzen)
 - Administration (Verwaltung)
 - Historical/Memorial (Historisches/Gedenken)
 - Other (Sonstiges)

Geographic Scope
 - District (Stadtbezirk)
 - City-wide (Gesamtstadt)
 - Regional (Regional)
 - National (National)
 - International (International)

Priority Level
 - Urgent (Dringend)
 - High (Hoch)
 - Medium (Mittel)
 - Low (Niedrig)

The Document Type should be one of the following:
 - Unbekannt
 - Anregungen und Beschwerden
 - Antrag
 - Beschlussvorlage
 - Informationsbrief
 - Mitteilungsvorlage
 - Stellungnahme der Verwaltung

"""


logfire.instrument_pydantic_ai()
logfire.instrument_anthropic()


@dataclass
class Deps:
    """
    A class representing the dependencies for the agent.
    """

    paper: Paper


agent = Agent(
    "claude-3-5-haiku-latest",
    deps_type=Deps,
    system_prompt=system_prompt,
    output_type=PaperAnalysis,
)


@agent.system_prompt
def add_paper_content(ctx: RunContext[Deps]) -> str:
    return f"This is the Markdown content of the Document: {ctx.deps.paper.content}."


@agent.system_prompt
def add_paper_metadata(ctx: RunContext[Deps]) -> str:
    return f"This is the metadata of the Document: {ctx.deps.paper.metadata}."


@agent.tool
async def retrieve(context: RunContext[Deps], search_query: str) -> str:
    """Retrieve documentation sections based on a search query.

    Args:
        context: The call context.
        search_query: The search query.
    """
    return ""


def analyze_document(paper: Paper) -> PaperAnalysis | None:
    """
    Analyze a document and return the analysis result.

    Parameters
    ----------
    paper : Paper
        The paper object to be analyzed.

    Returns
    -------
    DocumentAnalysis
        The analysis result, including metadata and categorization.
    """

    try:
        analysis = agent.run_sync("categorize the document", deps=Deps(paper=paper))
        logger.debug(f"Analysis result: {analysis}")

        logger.info(f"{analysis.output.id}: LLM usage: {analysis.usage()}")

        return analysis.output
    except Exception as e:
        logger.error(f"Error analyzing document: {e}")
        return None
    except KeyboardInterrupt:
        logger.info("Document analysis interrupted.")
        return None
    finally:
        logger.debug("Document analysis completed.")
