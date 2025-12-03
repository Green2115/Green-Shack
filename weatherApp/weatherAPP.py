from geopy.geocoders import Nominatim
import time
from pprint import pprint
from open_meteo import OpenMeteo
import asyncio
from datetime import datetime
import openmeteo_requests
from colorama import init, Fore, Back, Style
init(autoreset=True)
app = Nominatim(user_agent="tutorial")

#---Lat, lon---

def Get_Loc(address):
    time.sleep(1)
    try:
        result = app.geocode(address)
        if result is None:
            print("Location not found. Please try again.")
            address = input("Enter location: ")
            return Get_Loc(address)
        return result.raw
    except Exception as e:
        print(f"Error: {e}")
        address = input("Enter location: ")
        return Get_Loc(address)
    
address = input("Enter location: ")
location = Get_Loc(address)
longitude = location['lon']
latitude = location['lat']

#---end---

#---get the actual weather---

openmeteo = openmeteo_requests.Client()

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],
    "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
}
responses = openmeteo.weather_api(url, params=params)

response = responses[0]
print(Fore.RED+f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E" + "\n")
print(Fore.GREEN+f"Elevation: {response.Elevation()} m asl" + "\n")

current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()
hourly_wind_speed = current.Variables(2).Value()

current_time = datetime.fromtimestamp(current.Time())
print(Fore.GREEN+f"Current time: {current_time}" + "\n")
print(Fore.MAGENTA+f"Current temperature_2m: {round(current_temperature_2m, 3)} °C" + "\n")
print(Fore.RED+f"Current relative_humidity_2m: {round(current_relative_humidity_2m, 3)} %" + "\n")
print(Fore.BLUE+f"Current wind_speed_10m: {round(hourly_wind_speed, 3)} m/s")


#---end---