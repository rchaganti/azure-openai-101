from dotenv import load_dotenv
import os
import openai
from openai import AzureOpenAI
import json
import requests
import parsedatetime
from datetime import datetime
from pydantic import BaseModel

load_dotenv()

AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

class Suggestion(BaseModel):
    location: str
    date: str
    temperature: float
    cloth_suggestions: str

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

def parse_day(day_string):
    """
    Parses a day string and returns a datetime.date object.

    Args:
        day_string: The string to parse (e.g., "today", "tomorrow", "next Monday").

    Returns:
        date as a strning, or invalid input if the input is invalid.
    """
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(day_string)

    if parse_status == 0:
        return "Invalid input"

    return json.dumps({
        "day_string": day_string,
        "date": datetime(*time_struct[:6]).strftime("%Y-%m-%d")
    })

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather at a given location on a given date or current weather.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "The city name, e.g. Bengaluru",
                    },
                    "date": {
                        "type": "string",
                        "description": "Date on which the weather at the given location should be determined. This defaults to the current weather when a date is not specified.",
                    }
                },
                "required": ["city_name","date"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "parse_day",
            "description": "Get date from a text description",
            "parameters": {
                "type": "object",
                "properties": {
                    "day_string": {
                        "type": "string",
                        "description": "Text representation of date. eg., today, tomorrow, next friday, next monday, next week, and day after tomorrow.",
                    },
                },
                "required": ["day_string"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    }
]

def get_model_response(conversation_history):
    client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_ENDPOINT, 
    api_key = AZURE_OPENAI_API_KEY,  
    api_version = "2024-08-01-preview"
    )

    response = client.beta.chat.completions.parse(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=conversation_history,
        tools=tools,
        temperature=0.0,
        tool_choice="auto",
        response_format=Suggestion
    )

    return response

def get_tool_response(tool_name, tool_arguments):
    tools_args = json.loads(tool_arguments)                    
    tool_response = globals()[tool_name](**tools_args)
    return tool_response

if __name__ == "__main__":
    question = "I am going to Austin next week. Based on the weather, suggest what kind of cloths I need to carry."
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant. You should use the tools provided when needed to generate a response."},
        {"role": "user", "content": question}
    ]

    while True:
        response = get_model_response(conversation_history)
        response_message = response.choices[0].message

        if response_message.tool_calls:
            conversation_history.append({
                "role": "assistant", 
                "tool_calls": [tool_call.to_dict() for tool_call in response_message.tool_calls]
            })
            
            for tool_call in response_message.tool_calls:
                print(f"Tool call: {tool_call.function.name} with arguments: {tool_call.function.arguments}")
                tool_response = get_tool_response(tool_call.function.name, tool_call.function.arguments)
                conversation_history.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": tool_response
                    }
                )
        else:
            print(response_message.content)
            break