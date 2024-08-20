"""
vectore_store.py

This module sets up a connection to a Milvus vector store and provides functions to interact with it.
It includes functionality to retrieve all unique filenames stored in the metadata of a Milvus collection.
"""

from langchain.vectorstores.milvus import Milvus
from pymilvus import connections, Collection
from embeddings import embeddings

# Connection configuration for Milvus
connection = {
    "host": "127.0.0.1",
    "port": "19530",
    "user": "",
    "password": "",
    "secure": False,
}

# Initialize the Milvus vector store with the specified embedding function and connection arguments
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args=connection,
)


def get_all_unique_filenames():
    """
    Retrieve all unique filenames stored in the metadata of a Milvus collection.

    This function connects to the Milvus database, queries the specified collection for all entities,
    and extracts the filenames from the 'source' field of each entity. It returns a set of unique filenames.

    Returns:
    set: A set of unique filenames stored in the collection.
    """
    # Connect to the Milvus database
    connections.connect(
        db_name="default", host=connection["host"], port=connection["port"]
    )

    # Access the specified collection
    collection = Collection(name="LangChainCollection")

    # Query the collection for all entities and retrieve the 'source' field
    entities = collection.query(expr="pk > 0", output_fields=["source"])

    # Extract filenames from the 'source' field and return a set of unique filenames
    filenames = [entity["source"].split("/")[-1] for entity in entities]

    return set(filenames)
