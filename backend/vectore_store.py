from langchain.vectorstores.milvus import Milvus
from pymilvus import connections, Collection

from embeddings import embeddings

connection = {
    "host": "127.0.0.1",
    "port": "19530",
    "user": "",
    "password": "",
    "secure": False,
}

vector_store = Milvus(
    embedding_function=embeddings,
    connection_args=connection,
)


def get_all_unique_filenames():
    """Retrieve all filenames stored in the metadata of a Milvus collection."""
    connections.connect(
        db_name="default", host=connection["host"], port=connection["port"])

    collection = Collection(name="LangChainCollection")

    entities = collection.query(expr="pk > 0", output_fields=["source"])

    filenames = [entity["source"].split("/")[-1] for entity in entities]

    return set(filenames)
