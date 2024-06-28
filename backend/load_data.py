from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vectore_store import get_all_unique_filenames, vector_store, embeddings
import time
import glob
import warnings
import pymilvus


def load_data_dir(path: str):
    print(f"Loading data from {path} \n")

    start_time = time.time()

    pdf_files = glob.glob(f"{path}/*.pdf")
    for pdf_file in pdf_files:
        try:
            load_data_file(pdf_file)
        except ValueError as e:
            warnings.warn(f"Duplicate file skipped: {pdf_file}\n\n")
            continue  # Skip this document

    end_time = time.time()

    print(f"Embedding completed in {end_time - start_time} seconds")


def load_data_file(file_path: str, ):
    print(f"Loading data from {file_path}")

    filename = file_path.split("/")[-1]

    all_existing_files = []
    try:
        all_existing_files = get_all_unique_filenames()
    except pymilvus.exceptions.SchemaNotReadyException as e:
        print("No files found in the collection")

    if filename.split("/")[-1] in all_existing_files:
        raise ValueError(f"File {filename} already exists in the collection")

    start_time = time.time()

    loader = PyPDFLoader(file_path)

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=400, add_start_index=True)

    all_splits = text_splitter.split_documents(data)

    print(f"Loaded {len(all_splits)} splits")

    print("Starting to embed, this may take a while...")

    vector_store.from_documents(
        documents=all_splits,
        embedding=embeddings,
    )

    end_time = time.time()

    print(f"Embedding completed in {end_time - start_time} seconds\n")


if __name__ == "__main__":
    load_data_dir("data")
