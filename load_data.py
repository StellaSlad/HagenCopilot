from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_community.document_loaders.pdf import PyPDFLoader


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.jina import JinaEmbeddings
from langchain.vectorstores.milvus import Milvus

""" loader = DirectoryLoader(
    path="data",
    glob="*.pdf",
    show_progress=True,
    loader_cls=PyPDFLoader,
)

data = loader.load()

print(f"Loaded {len(data)} documents")


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)
"""

embeddings = JinaEmbeddings(
    jina_api_key="jina_f355babf70df438a9d36a6cd900b18cd5yNO44Bvk6FUXero10s_MIQ_godd", model_name="jina-embeddings-v2-base-de"
)

vector_store = Milvus(embedding_function=embeddings,
                      connection_args={
                          "host": "127.0.0.1",
                          "port": "19530",
                          "user": "",
                          "password": "",
                          "secure": False,
                      }
                      )


""" vector_store.from_documents(
    documents=all_splits, embedding=embeddings) """

# log how many vectors we have
print(f"Stored {vector_store.col.num_entities} vectors")
