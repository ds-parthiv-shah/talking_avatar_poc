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
#    if "I'm sorry" or "I'm unable" in resp:
#       response = client.completions.create(
#            model="gpt-3.5-turbo-instruct",
#            prompt=text_query,
#            max_tokens=256)
#       resp = response.choices[0].text.strip()

    if "I'm sorry" or "I'm unable" in resp:
         response = client.chat.completions.create(
         model="gpt-4",
         messages=[{"role": "user", "content": text_query}]
         )
         resp = response.choices[0].message.content        

    return jsonify({'Message': resp,'status':200})
    #return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
