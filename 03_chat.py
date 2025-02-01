from dotenv import load_dotenv
import os
from openai import AzureOpenAI
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
console = Console()

AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

client = AzureOpenAI(
  azure_endpoint = AZURE_OPENAI_ENDPOINT, 
  api_key = AZURE_OPENAI_API_KEY,  
  api_version = "2024-02-01"
)

response = client.chat.completions.create(
    model = AZURE_OPENAI_DEPLOYMENT_NAME,
    messages=[
        {"role": "system", "content": "You are a helpful tutor and an expert in Artificial Intelligence."},
        {"role": "user", "content": "How do I go about learning AI application development? Give me a roadmap."},
    ]
)

#print(response.choices[0].message.content)
md = Markdown(response.choices[0].message.content)
console.print(md)
