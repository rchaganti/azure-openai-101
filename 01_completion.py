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
    
start_phrase = 'What would be the tagline if Microsoft Azure was an ice cream shop?'
response = client.completions.create(
    model=AZURE_OPENAI_DEPLOYMENT_NAME_FOR_INSTRUCT, 
    prompt=start_phrase,
    max_tokens=30
)
print(start_phrase+response.choices[0].text)