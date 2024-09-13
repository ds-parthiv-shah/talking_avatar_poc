from dotenv import main
main.load_dotenv()
import os
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex, SimpleKeywordTableIndex
from llama_index.core import SummaryIndex
from llama_index.core import ComposableGraph
from llama_index.llms.openai import OpenAI
#from llama_index.core.response.notebook_utils import display_response
from llama_index.core import Settings
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache
#from llama_index.storage.index_store.redis import RedisIndexStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.redis import RedisVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.ingestion import (
    DocstoreStrategy,
    IngestionPipeline,
    IngestionCache,
)

documents = SimpleWebPageReader(html_to_text=True).load_data(["https://www.asterra.com.ph/articles/blog/a-quick-guide-to-thrift-banks-in-the-philippines"])
#index = SummaryIndex.from_documents(documents)
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
redis_password = 'e362uXIagvC1zgL01IdWRcINaQmjYebS'

def index_data(documents):
    # load documents with deterministic IDs
    #documents = SimpleDirectoryReader(data_folder, filename_as_id=True).load_data()
    llm = OpenAI(model="gpt-4", temperature=0.1)# When you set it lower, towards 0, the values are more deterministic.

    # Create a ServiceContext object with default configurations
    # This context incorporates required settings and services for generating vector representations
    embed_model = OpenAIEmbedding()
    #embed_model = "local:BAAI/bge-small-en-v1.5"
    #embed_model = "text-embedding-3-small"
    Settings.llm = llm
    Settings.embed_model = OpenAIEmbedding()
    embed_model = OpenAIEmbedding(model="text-embedding-3-small",)
    print('docs getting uploaded...')
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(),
            embed_model,
        ],
        docstore=RedisDocumentStore.from_host_and_port(
            REDIS_HOST, REDIS_PORT, namespace="talking_avatar"
        ),
        vector_store = RedisVectorStore(
        index_name="talking_avatar",
        index_prefix="llama",
        redis_url="redis://10.10.7.193:16489",  # Default
        #overwrite=True,
        #password = redis_password
    ),
        cache=IngestionCache(
            cache=RedisCache.from_host_and_port(REDIS_HOST, REDIS_PORT),
            collection="redis_cache",
        ),
        docstore_strategy=DocstoreStrategy.UPSERTS,
    )

    index = VectorStoreIndex.from_vector_store(
        pipeline.vector_store, embed_model=embed_model
    )

    nodes = pipeline.run(documents=documents)
    print(f"Ingested {len(nodes)} Nodes")
    return index

index = index_data(documents)
print("Documents and embeddings stored successfully!")
