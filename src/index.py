# Global
import os
from dotenv import main
main.load_dotenv()


import re

# Llama Index
from llama_index.core import SimpleDirectoryReader, Document, VectorStoreIndex, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.redis import RedisVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter


data_folder = "../data/"

# Create a SimpleDirectoryReader object to read data from the specified folder
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


def clean_text(text):
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text

# List comprehension to clean the text of each document in the 'documents' list
cleaned_documents = [clean_text(doc.text) for doc in documents]
document = Document(text="\n\n".join([doc for doc in cleaned_documents]))

text_content = document.get_text()

# Initialize an OpenAI language model (llm) with specific configurations
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1) # 0 to 2. When you set it higher, you'll get more random outputs.
                                                     # When you set it lower, towards 0, the values are more deterministic.

# Create a ServiceContext object with default configurations
# This context incorporates required settings and services for generating vector representations
embed_model = "text-embedding-3-small"
#embed_model = "local:BAAI/bge-small-en-v1.5"
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model=embed_model)
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)

vector_store = RedisVectorStore(
        index_name="talking_avatar",
        index_prefix="llama",
        redis_url="redis://10.10.7.193:16489",  # Default
        overwrite=True)

#vector_store.delete_index()

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# query_engine = index.as_query_engine()

# # Submit a Query String
# response = query_engine.query("Who is United States President?")

# print(str(response))
