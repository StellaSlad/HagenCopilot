"""
load_data.py

This module provides functions to load and process PDF files from a specified directory.
It uses the PyPDFLoader to read PDF files, splits the text into chunks, and embeds the text
into a vector store for further use in language models.
"""

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vectore_store import get_all_unique_filenames, vector_store, embeddings
import time
import glob
import pymilvus


def load_data_dir(path: str):
    """
    Load and process all PDF files from the specified directory.

    This function searches for all PDF files in the given directory, processes each file,
    and embeds the text into a vector store. If a file is already processed, it skips that file.

    Parameters:
    path (str): The directory path containing PDF files to be processed.

    Returns:
    None
    """
    print(f"Loading data from {path}")

    start_time = time.time()

    pdf_files = glob.glob(f"{path}/*.pdf")
    for pdf_file in pdf_files:
        try:
            load_data_file(pdf_file)
        except ValueError as e:
            print(f"Duplicate file skipped: {pdf_file}\n")
            continue  # Skip this document

    end_time = time.time()

    print(f"Embedding completed in {end_time - start_time} seconds\n")


def load_data_file(file_path: str):
    """
    Load and process a single PDF file.

    This function reads the PDF file, splits the text into chunks, and embeds the text into a vector store.
    If the file is already processed, it raises a ValueError.

    Parameters:
    file_path (str): The path to the PDF file to be processed.

    Returns:
    None

    Raises:
    ValueError: If the file already exists in the collection.
    """
    print(f"Loading data from {file_path}")

    filename = file_path.split("/")[-1]

    all_existing_files = []
    try:
        all_existing_files = get_all_unique_filenames()
    except pymilvus.exceptions.SchemaNotReadyException as e:
        print("No files found in the collection", e)

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
