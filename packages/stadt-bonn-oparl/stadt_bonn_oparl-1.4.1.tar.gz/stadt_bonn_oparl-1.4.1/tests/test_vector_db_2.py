import os
import sys


# Add the src directory to the Python path to allow importing stadt_bonn.oparl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from stadt_bonn.oparl.papers.vector_db import VectorDb


def main():
    db = VectorDb("test-1")
    print(f"VectorDb initialized. Collection: {db.collection.name}")

    print("\n--- Testing info() ---")
    db_info = db.info()
    print(f"DB Info: {db_info}")

    search_results = db.search_documents("Klärschlammverwertung")
    assert len(search_results) > 0
    for result in search_results:
        print(f"Search result: {result}")


if __name__ == "__main__":
    main()
