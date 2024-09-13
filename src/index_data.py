import os
from dotenv import main
main.load_dotenv()


import re

# Llama Index
from llama_index.core import SimpleDirectoryReader, Document, VectorStoreIndex, StorageContext
from llama_index.core.ingestion import (
    DocstoreStrategy,
    IngestionPipeline,
    IngestionCache,
)
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache

from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.redis import RedisVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import SubQuestionQueryEngine

redis_host = '10.10.7.193'
redis_port = 16489
redis_password = 'e362uXIagvC1zgL01IdWRcINaQmjYebS'

def clean_text(text):
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text
data_folder = "../data/"
reader = SimpleDirectoryReader(
        input_dir=data_folder,  # Set the input directory
        recursive=True,  # Enable recursive scanning through subdirectories
    )
# Create an empty list to store all documents
documents = []

# Iterate through the data returned by the reader and append each document to the 'documents' list
for docs in reader.iter_data():
    for doc in docs:
        documents.append(doc)

# List comprehension to clean the text of each document in the 'documents' list
cleaned_documents = [clean_text(doc.text) for doc in documents]
document = Document(text="\n\n".join([doc for doc in cleaned_documents]))
text_content = document.get_text()
#print(type(document))
#print(text_content)

# Initialize an OpenAI language model (llm) with specific configurations
#llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1) # 0 to 2. When you set it higher, you'll get more random outputs.
llm = OpenAI(model="gpt-4", temperature=0.1)# When you set it lower, towards 0, the values are more deterministic.

# Create a ServiceContext object with default configurations
# This context incorporates required settings and services for generating vector representations
embed_model = OpenAIEmbedding()
#embed_model = "local:BAAI/bge-small-en-v1.5"
#embed_model = "text-embedding-3-small"
Settings.llm = llm
Settings.embed_model = OpenAIEmbedding()
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
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
    #overwrite=True,
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

print("Documents and embeddings stored successfully!")
# query_engine = index.as_query_engine()
# response = query_engine.query("what is Integrari")
# print(response)
