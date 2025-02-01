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

