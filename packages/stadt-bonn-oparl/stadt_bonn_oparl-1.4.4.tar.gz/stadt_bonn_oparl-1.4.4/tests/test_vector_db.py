import json
import os
import sys
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel, DirectoryPath

# Add the src directory to the Python path to allow importing stadt_bonn.oparl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from stadt_bonn.oparl.papers.models import Paper
from stadt_bonn.oparl.papers.vector_db import VectorDb


class Ratsinformation(BaseModel):
    id: UUID
    metadata: dict
    content: str


def create_paper(data_path: DirectoryPath) -> Paper:
    """
    Create a Paper object from a directory path.
    """
    # Assuming the directory contains metadata.json and content.txt files
    metadata_path = data_path / "analysis.json"
    content_path = data_path.glob("*.md")  # Get the first markdown file
    content = ""

    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found in {data_path}")
    if not content_path:
        raise FileNotFoundError(f"No markdown files found in {data_path}")

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    for file in content_path:
        if file.suffix == ".md":
            with open(file, "r") as f:
                content = f.read()

    return Paper(id=metadata.get("id"), metadata=metadata, content=content)


def main():
    print("Starting VectorDB test program...")

    # Initialize VectorDb (in-memory by default)
    db = VectorDb()
    print(f"VectorDb initialized. Collection: {db.collection.name}")

    # 1. Test info method
    print("\n--- Testing info() ---")
    db_info = db.info()
    print(f"DB Info: {db_info}")
    assert db_info["status"] == "OK"
    assert db_info["collections"] >= 1

    # 2. Create a document
    print("\n--- Testing create_document() ---")

    # let's create Ratsinformation objects for all directories in data-1/
    data_path = Path("data-1/")
    for dir_path in data_path.iterdir():
        if dir_path.is_dir():
            try:
                rats_info = create_paper(dir_path)
                doc1_id = db.create_document(rats_info)  # noqa: F841
            except FileNotFoundError as e:
                print(e)

    db_info_after_create = db.info()
    print(f"DB Info after create: {db_info_after_create}")
    assert db_info_after_create["records"] == 13

    db_info = db.info()
    print(f"DB Info: {db_info}")

    # 5. Test search_drucksuchennummer
    print("\n--- Testing search_drucksuchennummer() ---")
    search_results = db.search_drucksuchennummer("Straßenentwässerungsanlage")
    assert len(search_results) > 0
    for result in search_results:
        assert isinstance(result, str)
        print(f"Search result: {result}")


if __name__ == "__main__":
    main()
