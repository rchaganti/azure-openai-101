from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

AZURE_OPENAI_API_KEY_FOR_INSTRUCT=os.getenv("AZURE_OPENAI_API_KEY_FOR_INSTRUCT")
AZURE_OPENAI_ENDPOINT_FOR_INSTRUCT=os.getenv("AZURE_OPENAI_ENDPOINT_FOR_INSTRUCT")
AZURE_OPENAI_DEPLOYMENT_NAME_FOR_INSTRUCT=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_FOR_INSTRUCT")
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY_FOR_INSTRUCT"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT_FOR_INSTRUCT")
)
    
start_phrase = 'What is the transformer architecture? Explain self-attention mechanism.'
response = client.completions.create(
    model=AZURE_OPENAI_DEPLOYMENT_NAME_FOR_INSTRUCT, 
    prompt=start_phrase,
    max_tokens=1000,
    stream=True
)

for chunk in response:
    if chunk.choices:
        if chunk.choices[0].finish_reason != 'stop':
            text = chunk.choices[0].text
            print(text, end='')