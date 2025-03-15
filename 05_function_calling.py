from dotenv import load_dotenv
import os
from openai import AzureOpenAI
import json
import requests
from datetime import datetime

load_dotenv()

AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

def get_weather(city_name, date=None):
    """
    Get the weather at a given location on a given date or current weather.

    Args:
        city_name: The city name, e.g. Bengaluru.
        date: Date on which the weather at the given location should be determined. This defaults to the current weather when a date is not specified.

    Returns:
        JSON string with the city name, date, and temperature.
    """
    api_key = os.getenv("VISUAL_CROSSING_API_KEY")
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    request_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}/{date}?unitGroup=metric&key={api_key}&contentType=json"
    response = requests.get(request_url)

    if response.status_code != 200:
        return json.dumps({
            "error": "Invalid city name or date"
        })
    else:
        respJson = response.json()
        return json.dumps({
            "city_name": city_name,
            "date": date,
            "temperature": respJson["days"][0]["temp"]
        })

def get_response(prompt):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather for a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city_name": {
                            "type": "string",
                            "description": "The city name, e.g. Bengaluru",
                        },
                    },
                    "required": ["city_name"],
                },
            }
        }
    ]

    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant. You should use the tools provided when needed to generate a response. When asked about the weather, return the response in Celsius."},
        {"role": "user", "content": prompt}
    ]

    client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT, 
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = "2024-02-01"
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=conversation_history,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
            conversation_history.append({
                "role": "assistant", 
                "tool_calls": [tool_call.to_dict() for tool_call in response_message.tool_calls]
            })
            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "get_weather":
                    function_args = json.loads(tool_call.function.arguments)                    
                    weather_response = get_weather(
                        city_name=function_args.get("city_name")
                    )

                    conversation_history.append({                        
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": "get_weather",
                        "content": weather_response,
                    })
                    final_response = client.chat.completions.create(
                        model=AZURE_OPENAI_DEPLOYMENT_NAME,
                        messages=conversation_history,
                        tools = tools,
                    )

                    return final_response.choices[0].message.content
    else:
        return response_message.content

if __name__ == "__main__":
  question = "What's the weather like in Bengaluru?"
  response = get_response(question)
  print(response)