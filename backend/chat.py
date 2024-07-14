from langchain_core.documents.base import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.llms.ollama import Ollama
from langchain_core.runnables import Runnable
import json
import os
from dotenv import load_dotenv

from vectore_store import vector_store
from prompt import PROMPT


def get_llm(model: str) -> Ollama:
    # Load the .env file
    if model is None:
        load_dotenv()
        model = os.getenv("MODEL")

    model_url = os.getenv("MODEL_URL")

    return Ollama(
        base_url=model_url,
        model=model,
    )


def get_retrival_chain(model: str = None) -> Runnable:
    llm = get_llm(model)
    retriever = vector_store.as_retriever(
        search_kwargs={'k': 5, 'fetch_k': 20})

    document_chain = create_stuff_documents_chain(llm, PROMPT)

    return create_retrieval_chain(retriever, document_chain)


class DocumentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Document):
            # Convert the Document object into a dictionary
            return obj.__dict__
        return super().default(obj)


def invoke(input: str, model: str = None):
    result = get_retrival_chain(model).invoke({"input": input})

    # converting the result to a json string
    json_result = json.dumps(result, cls=DocumentEncoder)

    # converting the json string to a dictionary
    dict_result = json.loads(json_result)
    return dict_result


if __name__ == "__main__":
    while True:
        query = input("\nQuestion: ")

        result = get_retrival_chain().invoke({"input": query})

        print("\nAnswer:")
        print(result["answer"])
