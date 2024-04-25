from dotenv import main
import os

main.load_dotenv()
from llama_index.core import SimpleDirectoryReader,VectorStoreIndex,StorageContext

from llama_index.core.ingestion import (
    DocstoreStrategy,
    IngestionPipeline,
    IngestionCache,
)
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.redis import RedisVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache
from llama_index.llms.openai import OpenAI

redis_host = '10.10.7.193'
redis_port = 16489
redis_password = 'e362uXIagvC1zgL01IdWRcINaQmjYebS'

def index_data(data_folder):
# load documents with deterministic IDs
    documents = SimpleDirectoryReader(data_folder, filename_as_id=True).load_data()

    llm = OpenAI(model="gpt-3.5-turbo")
    embed_model = OpenAIEmbedding(model="text-embedding-3-small",)

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(),
            embed_model,
        ],
        docstore=RedisDocumentStore.from_host_and_port(
            redis_host, redis_port, namespace="talking_avatar"
        ),
        vector_store = RedisVectorStore(
        index_name="talking_avatar",
        index_prefix="llama",
        redis_url="redis://10.10.7.193:16489",  # Default
        overwrite=True,
        #password = redis_password
    ),
        cache=IngestionCache(
            cache=RedisCache.from_host_and_port(redis_host, redis_port),
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

def query_response(query):
    vector_store = RedisVectorStore(index_name="talking_avatar",index_prefix="llama",redis_url="redis://10.10.7.193:16489")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response


# if __name__ == '__main__':
#     index = index_data('../data/')
#     print(index)
#     resp = query_response(index,'when will parthiv be 7 months and 8 days old?')
#     print(resp)
