import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask,jsonify,request
from flask_cors import CORS
from src.ingestion_pipeline import query_response
from openai import OpenAI
client = OpenAI()

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def process_text():
    # Get text from the request data
    data = request.json
    text_query = data['text']
    resp = str(query_response(text_query))
    specific_words = ["I'm sorry", "I'm unable","not explicitly defined","no information or context","no information","not mentioned"]

    # Check if specific words are contained in the response using list comprehension
    presence = [word for word in specific_words if word in resp]
    if  presence:
         print('From GPT4')
         response = client.chat.completions.create(
         model="gpt-4-turbo",
         messages=[{"role": "user", "content": text_query}],
         max_tokens = 128
         
         )
         resp = response.choices[0].message.content        

    return jsonify({'Message': resp,'status':200})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
