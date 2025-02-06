from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

client = AzureOpenAI(
  azure_endpoint = AZURE_OPENAI_ENDPOINT, 
  api_key = AZURE_OPENAI_API_KEY,  
  api_version = "2024-02-01"
)

conversation_history = [
    {"role": "system", "content": "You are a helpful tutor and an expert in Artificial Intelligence. You should provide a tabular output when the user asks to compare two things."},
]

while True:
    user_prompt = input("\nYou: ")
    if user_prompt.lower() == "exit":
        break
    conversation_history.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
        model = AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=conversation_history
    )

    assistant_message = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_message})

    print("\nAssistant: " + assistant_message)