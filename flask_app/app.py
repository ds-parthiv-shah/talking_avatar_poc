# app.py
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, render_template, request, redirect, url_for
import subprocess

from src.speech_to_text import speech2text
from src.ingestion_pipeline import index_data,query_response
from src.text_to_avatar import *

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_type = request.form['input_type']

    if input_type == 'speech':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            index = index_data('../data/')
            text_query = speech2text(filepath)
            resp = str(query_response(text_query))
            id= get_response(resp)
            response = check_video_generation_status(id)
            print(response)
            #file.save(filepath)
    else:
        text_query = request.form['text']
        resp = str(query_response(text_query))
        print(resp)
        # Process text

    # Process input and generate video
    # For demonstration, let's assume we generate a placeholder video
    subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=5:size=320x240:rate=30', 'output.mp4'])

    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
