from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections
from dotenv import load_dotenv
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.milvus import Milvus
import os

# Load the .env file
load_dotenv()

model_url = os.getenv("FUH_VPN_URL")
model = os.getenv("MODEL")

loader = DirectoryLoader(
    path="data",
    glob="*.pdf",
    show_progress=True,
    loader_cls=PyPDFLoader,
)

data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=300, add_start_index=True)

all_splits = text_splitter.split_documents(data)

print(f"Loaded {len(all_splits)} splits")

print("Starting to embed, this may take a while...")
ollama_emb = OllamaEmbeddings(
    base_url=model_url,
    model=model,
)


vector_store = Milvus(
    embedding_function=ollama_emb,
    drop_old=True,
    connection_args={
        "host": "127.0.0.1",
        "port": "19530",
        "user": "",
        "password": "",
        "secure": False,
    }
).from_documents(
    documents=all_splits,
    embedding=ollama_emb
)
