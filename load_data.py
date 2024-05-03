from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.jina import JinaEmbeddings
from langchain.vectorstores.milvus import Milvus

loader = PyPDFLoader(
    file_path="data/modulhandbuch.pdf",
)
data = loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

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


result = vector_store.from_documents(documents=all_splits, embedding=embeddings) 
print(result)

print(vector_store.search("Fachbereich", search_type="similarity"))
