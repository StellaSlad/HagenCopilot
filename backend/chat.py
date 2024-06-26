from langchain_core.documents.base import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.llms.ollama import Ollama
import json
import os
from dotenv import load_dotenv

from vectore_store import vector_store
from prompt import PROMPT

# Load the .env file
load_dotenv()

model_url = os.getenv("MODEL_URL")
model = os.getenv("MODEL")

llm = Ollama(
    base_url=model_url,
    model=model,
)

retriever = vector_store.as_retriever(
    search_kwargs={'k': 5, 'fetch_k': 20})

document_chain = create_stuff_documents_chain(llm, PROMPT)

retrieval_chain = create_retrieval_chain(retriever, document_chain)


class DocumentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Document):
            # Convert the Document object into a dictionary
            return obj.__dict__
        return super().default(obj)


def invoke(input: str):
    result = retrieval_chain.invoke({"input": input})

    # converting the result to a json string
    json_result = json.dumps(result, cls=DocumentEncoder)

    # converting the json string to a dictionary
    dict_result = json.loads(json_result)
    return dict_result


if __name__ == "__main__":
    while True:
        query = input("\nQuestion: ")

        result = retrieval_chain.invoke({"input": query})

        print("\nAnswer:")
        print(result["answer"])
