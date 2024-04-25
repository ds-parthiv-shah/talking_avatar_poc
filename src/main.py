from speech_to_text import speech2text
from ingestion_pipeline import index_data,query_response
from text_to_avatar import *
import time
from dotenv import main
from openai import OpenAI
client = OpenAI()

main.load_dotenv()

if __name__=='__main__':
    start = time.time()
    
    text_query = 'What is topup in mobifin?'
    resp = str(query_response(text_query))
    specific_words = ["I'm sorry", "I'm unable","not explicitly defined","no information or context","no information","not mentioned"]

    # Check if specific words are contained in the response using list comprehension
    presence = [word for word in specific_words if word in resp]
    if  presence:
         print('From GPT4')
         response = client.chat.completions.create(
         model="gpt-4",
         messages=[{"role": "user", "content": text_query}]
         )
         resp = response.choices[0].message.content        

    end = time.time()
    print('\nTime taken :',(end-start))
    print(resp)

