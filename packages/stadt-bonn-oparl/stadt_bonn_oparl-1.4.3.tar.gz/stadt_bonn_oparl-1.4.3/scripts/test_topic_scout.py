# test our topic scout agent

import asyncio
import json

from pydantic import DirectoryPath
from pydantic_ai.usage import UsageLimits
import rich

from stadt_bonn_oparl.agents.topic_scout import Deps, agent
from stadt_bonn_oparl.agents.topic_scout import (
    user_prompt_template as topic_scout_user_prompt,
)
from stadt_bonn_oparl.logging import configure_logging
from stadt_bonn_oparl.papers.models import UnifiedPaper
from stadt_bonn_oparl.papers.vector_db import VectorDb


def create_paper(data_path: DirectoryPath) -> UnifiedPaper:
    """
    Create a Paper object from a directory path.
    """
    # Assuming the directory contains metadata.json and content.txt files
    metadata_path = data_path / "metadata.json"
    analysis_path = data_path / "analysis.json"
    content_path = data_path.glob("*.md")  # Get the first markdown file
    content = ""
    analysis = {}
    metadata = {}

    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found in {data_path}")
    if not content_path:
        raise FileNotFoundError(f"No markdown files found in {data_path}")

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    with open(analysis_path, "r") as f:
        analysis = json.load(f)

    for file in content_path:
        if file.suffix == ".md":
            with open(file, "r") as f:
                content = f.read()

    return UnifiedPaper(
        paper_id=metadata.get("id"),
        metadata=metadata,
        markdown_text=content,
        analysis=analysis,
        enrichment_status="enriched",
        external_oparl_data={},
    )


configure_logging(2)

db = VectorDb("test-100")


async def main():
    db_info_after_create = db.info()
    print(f"DB Info after create: {db_info_after_create}")

    topic = "Politische Bildung von Kindern und Jugendlichen"
    topic = "Steuerliche Anreize für die Schaffung von Wohnraum"
    topic = "förderung des radverkehrs in bonn"

    async with agent.run_mcp_servers():
        deps = Deps(topic=topic, vector_db_name="test-100")
        user_prompt = topic_scout_user_prompt.replace("{THEMA}", topic)
        result = await agent.run(
            user_prompt=user_prompt,
            deps=deps,
            usage_limits=UsageLimits(None),
        )

        rich.print(result.output)
        rich.print(result.usage())

        # save the result to a file
        with open("test_topic_scout_result.json", "w") as f:
            f.write(result.output.model_dump_json(by_alias=True, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
