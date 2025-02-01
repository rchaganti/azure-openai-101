# import required modules
import requests
import json
import os
from dotenv import load_dotenv
 
load_dotenv()

api_key = os.getenv("OPEN_WEATHER_API_KEY")
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = input("Enter city name : ")
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
 
response = requests.get(complete_url)
x = response.json()

if x["cod"] != "404":
    y = x["main"]
    current_temperature = y["temp"]
    current_pressure = y["pressure"]
    current_humidity = y["humidity"]
    z = x["weather"]
    weather_description = z[0]["description"]
 
    print(" Temperature (in Celcius unit) = " +
                    str(int(current_temperature - 273.15)))
else:
    print(" City Not Found ")
