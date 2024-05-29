from langchain.vectorstores.milvus import Milvus
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

embedding = HuggingFaceBgeEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)


vector_store = Milvus(
    embedding_function=embedding,
    connection_args={
        "host": "127.0.0.1",
        "port": "19530",
        "user": "",
        "password": "",
        "secure": False,
    }
)
