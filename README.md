
# Talking avatar (backend poc)

Introducing Our Revolutionary Talking Avatar: Powered by RAG, LlamaIndex, Redis DB, and OpenAI LLM

At the heart of our Talking Avatar is RAG (Retrieval-Augmented Generation), an advanced natural language processing model that combines the power of retrieval-based and generative AI techniques. RAG allows our avatar to retrieve relevant information from vast knowledge bases and generate contextually relevant responses in real-time, enabling fluid and engaging conversations with users.
![avatar](https://github.com/ds-parthiv-shah/talking_avatar_poc/assets/117074142/26774c6a-51ea-4d8b-b646-4849befa20a9)

## Installation


### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`OPENAI_API_KEY`



### Install requirements

Install with pip

```bash
  pip install -r requirements.txt
```

## Start server   
This will start flask server on port 5000
```bash
  cd flask_app
  python hello.py
```

## Postman

Set auth key
![auth](https://github.com/ds-parthiv-shah/talking_avatar_poc/assets/117074142/05802012-664f-4010-90b1-60b2ab2d4295)


Get response from RAG
![rag_resp](https://github.com/ds-parthiv-shah/talking_avatar_poc/assets/117074142/aeff0528-901a-4700-b3c9-f0b0f1f88c19)


Response from GPT model
![gpt_resp](https://github.com/ds-parthiv-shah/talking_avatar_poc/assets/117074142/5d7524d3-1b73-443f-a511-391c616146de)


## Demo URL
https://virtualagent.panamaxil.com/
