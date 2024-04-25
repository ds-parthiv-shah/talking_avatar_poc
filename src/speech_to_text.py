from dotenv import main

main.load_dotenv()
from openai import OpenAI
client = OpenAI()

def speech2text(file):
    audio_file= open(file, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription.text