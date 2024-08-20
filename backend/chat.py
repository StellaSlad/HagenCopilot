"""
chat.py

This module provides functionality to interact with a language model using a retrieval-based approach.
It sets up the language model, constructs retrieval chains, and processes user queries to generate responses.

Usage:
    Run this script directly to enter an interactive question-answer loop with the language model.
"""

from dotenv import load_dotenv
from langchain_core.documents.base import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.llms.ollama import Ollama
from langchain_core.runnables import Runnable
import json
import os

from vectore_store import vector_store
from prompt import PROMPT


def get_llm(model: str) -> Ollama:
    """
    Initialize and return an Ollama language model instance.

    This function loads environment variables, retrieves the model URL, and initializes the Ollama model.

    Parameters:
    model (str): The name of the model to be used.

    Returns:
    Ollama: An instance of the Ollama language model.
    """
    load_dotenv()
    model_url = os.getenv("MODEL_URL")

    return Ollama(
        base_url=model_url,
        model=model,
    )


def get_retrival_chain(model: str = None) -> Runnable:
    """
    Create and return a retrieval chain.

    This function sets up a retriever using the vector store, creates a document chain with the language model and prompt,
    and combines them into a retrieval chain.

    Parameters:
    model (str, optional): The name of the model to be used. Defaults to None.

    Returns:
    Runnable: A runnable retrieval chain.
    """
    llm = get_llm(model)
    retriever = vector_store.as_retriever(
        search_kwargs={'k': 5, 'fetch_k': 20})

    document_chain = create_stuff_documents_chain(llm, PROMPT)

    return create_retrieval_chain(retriever, document_chain)


class DocumentEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for Document objects.

    This class extends the default JSONEncoder to handle Document objects by converting them into dictionaries.
    """

    def default(self, o):
        if isinstance(o, Document):
            # Convert the Document object into a dictionary
            return o.__dict__
        return super().default(o)


def invoke(query: str, model: str = None) -> dict:
    """
    Process the input query using the retrieval chain and return the result.

    This function invokes the retrieval chain with the query, converts the result to a JSON string,
    and then parses it back into a dictionary.

    Parameters:
    query (str): The input query to be processed.
    model (str, optional): The name of the model to be used. Defaults to None.

    Returns:
    dict: The result of the query as a dictionary.
    """
    result = get_retrival_chain(model).invoke({"input": query})

    # converting the result to a json string
    json_result = json.dumps(result, cls=DocumentEncoder)

    # converting the json string to a dictionary
    dict_result = json.loads(json_result)
    return dict_result


if __name__ == "__main__":
    while True:
        q = input("\nQuestion: ")

        res = get_retrival_chain().invoke(
            {"input": q}, model="llama3:latest")

        print("\nAnswer:")
        print(res["answer"])
