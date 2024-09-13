import redis
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.web import SimpleWebPageReader
from llama_index.vector_stores.redis import RedisVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex, StorageContext

parser = SentenceSplitter()
# Connect to Redis
redis_client = redis.StrictRedis(
    host='10.10.7.193',
    port=16489,
    password='e362uXIagvC1zgL01IdWRcINaQmjYebS',
    decode_responses=True
)

# Initialize Redis vector store
vector_store = RedisVectorStore(
    index_name="talking_avatar",
    index_prefix="llama",
    redis_url="redis://10.10.7.193:16489",)
    
def add_webpage_documents(url):
    # Read and process data from a URL
    reader = SimpleWebPageReader()
    documents = reader.load_data([url])
    nodes = [parser.get_nodes_from_documents(text=doc['text']) for doc in documents]

    # Add documents to Redis
    for node in nodes:
        vector_store.add_document(node)

def add_directory_documents(directory_path):
    # Read and process data from a directory
    reader = SimpleDirectoryReader(directory_path)
    documents = reader.load_data()
    nodes = [parser.get_nodes_from_documents(text=doc['text']) for doc in documents]

    # Add documents to Redis
    for node in nodes:
        vector_store.add_document(node)

# Example usage
url = 'https://www.asterra.com.ph/articles/blog/a-quick-guide-to-thrift-banks-in-the-philippines'
directory_path = '../phillipines_data/'

add_webpage_documents(url)
add_directory_documents(directory_path)

# To query the data
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
print("Done!")
