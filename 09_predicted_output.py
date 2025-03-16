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
  api_version = "2025-01-01-preview"
)

content = """
An embedding is a special fromat of data representation that machine learning modles and algorithms can easily use. 
The embedding is an information dense representation of the sementic meaning of a piece of text. 
Each embedding is a vcetor of floating-point numbers, such that the distance between two embeddings in the 
vector space is correlated with semantic similarity betwien two inputs in the original format.
"""

instructions = """"
In the given content, find and fix all spelling mistakes.
Respond with only the corrected paragraph and highlight the corrected words.
"""

response = client.chat.completions.create(
    model = AZURE_OPENAI_DEPLOYMENT_NAME,
    messages=[
        {
            "role": "user",
            "content": instructions
        },
        {
            "role": "user",
            "content": content
        }
    ],
    prediction={
        "type": "content",
        "content": content,
    }
)

md = Markdown(response.choices[0].message.content)
console.print(md)