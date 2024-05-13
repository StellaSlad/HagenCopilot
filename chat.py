from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.vectorstores.milvus import Milvus
from langchain_community.llms.ollama import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv

from prompt import QA_CHAIN_PROMPT

# Load the .env file
load_dotenv()

model_url = os.getenv("FUH_VPN_URL")
model = os.getenv("MODEL")

llm = Ollama(
    base_url=model_url,
    model="mixtral",
    callback_manager=CallbackManager(
        [StreamingStdOutCallbackHandler()]
    ),
    stop=["<|eot_id|>"]
)


ollama_emb = OllamaEmbeddings(
    base_url=model_url,
    model=model,
)
vector_store = Milvus(embedding_function=ollama_emb,
                      connection_args={
                          "host": "127.0.0.1",
                          "port": "19530",
                          "user": "",
                          "password": "",
                          "secure": False,
                      }
                      )


retriever = vector_store.as_retriever(search_kwargs={"k": 20})


combine_docs_chain = create_stuff_documents_chain(
    llm, QA_CHAIN_PROMPT
)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

if __name__ == "__main__":
    while True:
        query = input("\nQuery: ")

        result = retrieval_chain.invoke({"input": query})
        print("")
        print(result)
