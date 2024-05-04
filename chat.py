from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.embeddings.jina import JinaEmbeddings
from langchain.vectorstores.milvus import Milvus
from langchain_community.llms.ollama import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from prompt import QA_CHAIN_PROMPT

llm = Ollama(
    model="llama3",
    callback_manager=CallbackManager(
        [StreamingStdOutCallbackHandler()]
    ),
    stop=["<|eot_id|>"],
)

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


retriever = vector_store.as_retriever(search_kwargs={"fetch_k": 10})


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
