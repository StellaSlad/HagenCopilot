from langchain.vectorstores.milvus import Milvus
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from pymilvus import connections, Collection

embedding = HuggingFaceBgeEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

connection = {
    "host": "127.0.0.1",
    "port": "19530",
    "user": "",
    "password": "",
    "secure": False,
}

vector_store = Milvus(
    embedding_function=embedding,
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
