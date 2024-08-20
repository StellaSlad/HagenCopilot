"""
embeddings.py

This module initializes the HuggingFaceBgeEmbeddings for use in embedding text data.
The embeddings are configured to use the "intfloat/multilingual-e5-large" model, which supports multiple languages.
The embeddings are normalized and set to run on the CPU, this can be changed to run on a GPU if available or MPS on M1 chips.

"""

from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# Initialize the HuggingFaceBgeEmbeddings with the specified model and settings
embeddings = HuggingFaceBgeEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
