"""
This script handles multi language query and response.
LLM : GPT-4
"""
import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI as opai
from llama_index.vector_stores.redis import RedisVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.llms.openai import OpenAI
from concurrent_log_handler import ConcurrentRotatingFileHandler


# Initialize OpenAI client
client = opai()

app = Flask(__name__)
CORS(app)

if not os.path.exists('/home/ubuntu/project/poc/talking_avatar/logs'):
    os.makedirs('/home/ubuntu/project/poc/talking_avatar/logs')

# Set up file handler for logging
file_handler = ConcurrentRotatingFileHandler('/home/ubuntu/project/poc/talking_avatar/logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'))

# Add the file handler to the app's logger
app.logger.addHandler(file_handler)

# Set the Flask app logger level to INFO
app.logger.setLevel(logging.INFO)

llm = OpenAI(model="gpt-4", temperature=0.1)

# Define query_response function
def query_response(query):
    vector_store = RedisVectorStore(index_name="talking_avatar", index_prefix="llama", redis_url="redis://10.10.7.193:16489")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    query_engine = index.as_query_engine(llm=llm)
    response = query_engine.query(query)
    return response

@app.route('/query', methods=['POST'])
def process_text():
    try:
        # Get text from the request data
        data = request.json
        if 'lang' in data:
            language_name = data['lang']
            text_query = data['text'] + f" Give response in {language_name} language"
        else:
            text_query = data['text']
        # Get the response from LlamaIndex
        response = str(query_response(text_query))

        specific_words = [
            "I'm sorry", "I'm unable", "not explicitly defined", "no information or context", 
            "no information", "not mentioned", "I am unable", "The context provided does not contain",
            "Sorry","Pasensya na","Pasensya","The context",
        ]

        # Check if specific words are contained in the response
        presence = [word for word in specific_words if word in response]
        if presence:
            gpt_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": text_query}],
                max_tokens=512
            )
            response = gpt_response.choices[0].message.content

        return jsonify({'Message': response,'status':200})
    except Exception as e:
        app.logger.exception(f"Exception occurred in process_text: {e}")
        return jsonify({'error': 'An error occurred while processing the request.', 'status': 500})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
