from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vectore_store import vector_store, embedding
import time


def load_data(path: str):
    print(f"Loading data from {path}")

    start_time = time.time()

    loader = DirectoryLoader(
        path=path,
        glob="*.pdf",
        show_progress=True,
        loader_cls=PyPDFLoader,
    )

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True)

    all_splits = text_splitter.split_documents(data)

    print(f"Loaded {len(all_splits)} splits")

    print("Starting to embed, this may take a while...")

    vector_store.from_documents(
        documents=all_splits,
        embedding=embedding,

    )

    end_time = time.time()

    print(f"Embedding completed in {end_time - start_time} seconds")


if __name__ == "__main__":
    load_data("data")
