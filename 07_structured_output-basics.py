from dotenv import load_dotenv
from pydantic import BaseModel
from openai import AzureOpenAI
import os

load_dotenv()

AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

client = AzureOpenAI(
  azure_endpoint = AZURE_OPENAI_ENDPOINT, 
  api_key = AZURE_OPENAI_API_KEY,  
  api_version = "2024-08-01-preview"
)

class TravelPlan(BaseModel):
    city_name: str
    date: str

response = client.beta.chat.completions.parse(
    model=AZURE_OPENAI_DEPLOYMENT_NAME,
    messages=[
        {"role": "system", "content": "Extract the city and travel information."},
        {"role": "user", "content": "I will be travelling to London next week."},
    ],
    response_format=TravelPlan,
)

stuctured_output = response.choices[0].message.parsed

print(stuctured_output)
print(response.choices[0].message.content)