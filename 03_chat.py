from dotenv import load_dotenv
import os
from openai import AzureOpenAI
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()
console = Console()

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-01"
)

response = client.chat.completions.create(
    model="gpt-40",
    messages=[
        {"role": "system", "content": "You are a helpful tutor and an expert in Artificial Intelligence."},
        {"role": "user", "content": "How do I go about learning AI application development? Give me a roadmap."},
    ]
)

#print(response.choices[0].message.content)
md = Markdown(response.choices[0].message.content)
console.print(md)
