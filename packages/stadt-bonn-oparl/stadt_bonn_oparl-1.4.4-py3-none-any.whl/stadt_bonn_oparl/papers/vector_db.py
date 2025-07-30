import importlib
import uuid
from typing import List, Optional, Tuple

import chromadb
from loguru import logger
from pydantic import BaseModel, DirectoryPath

from stadt_bonn_oparl.papers.models import UnifiedPaper


class VectorDb:
    """
    Vector database access class that abstracts ChromaDB implementation details.
    Provides methods to create, retrieve, and update documents.
    """

    def __init__(self, client: str | DirectoryPath = "memory"):
        """
        Initialize the vector database with an in-memory ChromaDB instance.

        Args:
            client (str | DirectoryPath): The type of ChromaDB client to use. Options are:
                - "memory": In-memory client (EphemeralClient)
                - "<path>": Path to the persistent storage directory
        """
        # Initialize in-memory ChromaDB client using the new API
        if client == "memory":
            self.client = chromadb.EphemeralClient()
        else:
            self.client = chromadb.PersistentClient(
                path=str(client),
            )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="stadt_bonn_oparl_papers"
        )

    def create_document(self, document: UnifiedPaper) -> str:
        """
        Create a new document or model in the vector database.

        Args:
            document (UnifiedPaper): The Pydantic model to create

        Returns:
            str: The ID of the created document/model
        """
        # Generate a unique ID
        doc_id = str(uuid.uuid4())

        # Get fully qualified class name for the model
        model_class_name = (
            f"{document.__class__.__module__}.{document.__class__.__name__}"
        )

        # convert metadata.key_stakeeholders to a string
        if "key_stakeholders" in document.metadata:
            document.metadata["key_stakeholders"] = ", ".join(
                document.metadata["key_stakeholders"]
            )

        # convert metadata.tags to a string
        if "tags" in document.metadata:
            document.metadata["tags"] = ", ".join(document.metadata["tags"])

        # Use Pydantic's model_dump_json for serialization
        json_content = document.model_dump_json(indent=2)
        metadatas = {
            "model_type": model_class_name,
            **document.metadata,
        }

        # keep everything in metadatas that is a str, rest gets filtered out
        metadatas = {
            k: v
            for k, v in metadatas.items()
            if isinstance(v, str) or isinstance(v, int) or isinstance(v, float)
        }

        # Store document with metadata containing model type information
        self.collection.add(
            ids=[doc_id],
            documents=[json_content],
            metadatas=[metadatas],
        )

        return doc_id

    def list_documents(self) -> List[Tuple[str, UnifiedPaper]]:
        """
        List all documents in the vector database and reconstruct their original model types.

        Returns:
            List[Tuple[str, UnifiedPaper]]: A list of (document ID, model) tuples.
        """
        results = self.collection.get(include=["documents", "metadatas"])
        ids = results.get("ids", [])
        documents = results.get("documents") or []
        metadatas = results.get("metadatas") or []

        document_list = []
        for doc_id, content, metadata in zip(ids, documents, metadatas):
            if metadata and "model_type" in metadata:
                model = self._reconstruct_model(
                    str(metadata["model_type"]), content, doc_id
                )
                document_list.append((doc_id, model))
            else:
                # If no model type is found, we cannot reconstruct the model
                logger.error(f"Model type not found for document ID {doc_id}")

        return document_list

    def retrieve_document(self, doc_id: str) -> Optional[UnifiedPaper]:
        """
        Retrieve a document by ID and reconstruct the original Pydantic model.

        Args:
            doc_id (str): The ID of the document to retrieve

        Returns:
            Optional[BaseModel]: The retrieved document as its original model type,
                                 or None if not found
        """
        # Get document from collection with metadata
        results = self.collection.get(ids=[doc_id], include=["documents", "metadatas"])

        # Check if document exists and has required data
        documents = results.get("documents", [])
        if not results or not results.get("ids") or not documents:
            return None

        # Extract content
        content = documents[0]

        metadatas = results.get("metadatas", [])
        if metadatas and metadatas[0] and isinstance(metadatas[0], dict):
            model_type_value = metadatas[0].get("model_type")
            if model_type_value and isinstance(model_type_value, str):
                model_type = model_type_value
                return self._reconstruct_model(model_type, content, doc_id)

    def _reconstruct_model(
        self, model_type: str, content: str, id: str
    ) -> UnifiedPaper:
        """
        Dynamically import and reconstruct a Pydantic model from its class name and content.

        Since all models are in the konsensgraph.models module, we can simplify import logic.

        Args:
            model_type (str): Fully qualified class name (module.ClassName)
            content (str): JSON string representation of the model

        Returns:
            Paper: Reconstructed Pydantic model
        """

        try:
            # Split module and class name
            module_name, class_name = model_type.rsplit(".", 1)

            module = importlib.import_module(module_name)

            # Get the class
            model_class = getattr(module, class_name)

            m = model_class.model_validate_json(content)

            # reconstruct key_stakeholders and tags as lists
            if "key_stakeholders" in m.metadata:
                m.metadata["key_stakeholders"] = m.metadata["key_stakeholders"].split(
                    ", "
                )
            if "tags" in m.metadata:
                m.metadata["tags"] = m.metadata["tags"].split(", ")

            return m
        except Exception as e:
            # If anything goes wrong, log the error and re-raise
            logger.error(f"Error reconstructing model {model_type}: {e}")
            raise

    def update_document(self, doc_id: str, document: BaseModel) -> bool:
        """
        Update an existing document.

        Args:
            doc_id (str): The ID of the document to update
            document (BaseModel): The new document content

        Returns:
            bool: True if the document was updated, False if it doesn't exist
        """
        # Check if document exists
        results = self.collection.get(ids=[doc_id])
        if not results["ids"]:
            return False

        # Get fully qualified class name for the model
        model_class_name = (
            f"{document.__class__.__module__}.{document.__class__.__name__}"
        )

        # Convert model to JSON
        json_content = document.model_dump_json(indent=2)

        # Update document with metadata containing model type information
        self.collection.update(
            ids=[doc_id],
            documents=[json_content],
            metadatas=[{"model_type": model_class_name}],
        )

        return True

    def search_documents(self, query: str) -> list[UnifiedPaper]:
        """
        Search for documents matching the query.

        Args:
            query (str): The search query

        Returns:
            list[UnifiedPaper]: A list of matching documents
        """
        logger.debug(f"Searching for documents with query: {query}")
        results = self.collection.query(
            query_texts=[query], n_results=5, include=["documents"]
        )
        logger.debug(f"Search results: {results}")

        # lets retrieve all documents and return them as a list of models
        ids = results.get("ids", [])[0]
        logger.info(f"IDs: {ids}")

        document_list = []
        for doc_id in ids:
            # Get document from collection with metadata
            doc = self.retrieve_document(doc_id)
            if doc:
                document_list.append(doc)

        return document_list

    def search_drucksuchennummer(self, query: str) -> list[str]:
        """
        Search for documents matching the query and return their Paper IDs (Drucksachennummer).

        Args:
            query (str): The search query

        Returns:
            list[str]: A list of matching document IDs
        """
        results = self.collection.query(
            query_texts=[query], n_results=5, include=["metadatas"]
        )

        # get all the ids from the metadatas
        ids = []

        metadatas = results.get("metadatas", [])
        if metadatas is None:
            metadatas = []

        for metadata in metadatas[0]:
            if metadata and isinstance(metadata, dict):
                # Check if the metadata contains the key "id"
                if "id" in metadata:
                    ids.append(metadata["id"])
                else:
                    logger.error(f"ID not found in metadata: {metadata}")
            else:
                logger.error(f"Invalid metadata format: {metadata}")

        return ids

    def info(self) -> dict:
        """
        Get information about the ChromaDB instance.

        Returns:
            dict: Information including path/URI, number of collections, number of records,
                ChromaDB version, and status.

        Example:
            {
                "path": "in-memory",
                "collections": 1,
                "records": 42,
                "version": "0.4.22",
                "status": "OK"
            }
        """
        from loguru import logger

        info = {}
        try:
            # Path/URI: EphemeralClient is always in-memory
            info["path"] = "in-memory"

            # Number of collections
            collections = self.client.list_collections()
            info["collections"] = len(collections)

            # Number of records in the main collection
            info["records"] = self.collection.count()

            # ChromaDB version
            try:
                import chromadb

                info["version"] = getattr(chromadb, "__version__", "unknown")
            except Exception as e:
                logger.warning(f"Could not get ChromaDB version: {e}")
                info["version"] = "unknown"

            info["status"] = "OK"
        except Exception as e:
            logger.error(f"Error retrieving ChromaDB info: {e}")
            info["status"] = f"ERROR: {e}"

        return info
