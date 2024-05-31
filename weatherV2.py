import datetime
import requests
import json
from easygui import *
address = ""
buttons = ["Exit"]
f = open ('config.json', 'r')
config = json.load(f)
def geocode_location(address):
    url = f"https://api.maptiler.com/geocoding/{address}.json"
    params = {
        'key': config.get('api_key')
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'features' in data and len(data['features']) > 0:
            coordinates = data['features'][0]['geometry']['coordinates']
            place_name = data['features'][0]['place_name']
            return place_name, coordinates

        else:
            return None

    else:
        response.raise_for_status()

while address == "":
        address = enterbox("Enter Location: ")
        if address == "":
           msgbox("Location cannot be empty, please type something.")
        elif address == None:
            exit()
        elif address.lower() == "something":
            msgbox("I swear to fucking god.")
            exit()

place_name, coordinates = geocode_location(address)
if address != "" or None:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	    "latitude": coordinates[1],
	    "longitude": coordinates[0],
	    "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"]
    }
    get = requests.get(url, params=params).json()
    pressed = buttonbox(f"Temperature: {str(get['current']['temperature_2m'])}C°\n"f"Humidity: {str(get['current']['relative_humidity_2m'])}%\n"f"Wind Speed: {str(get['current']['wind_speed_10m'])}m/s",choices=buttons,title=f"Weather in {place_name}")

if pressed == "Exit":
    try:
        with open("log.txt", "r", encoding="UTF-8") as f:
            is_empty = f.read(1) == ''
    except FileNotFoundError:
        is_empty = True

    aeg = datetime.datetime.now()
    f = open("log.txt", "a", encoding="UTF-8")
    if not is_empty:
        f.write("\n")
    f.write(f"Location: {place_name} \n")
    f.write(f"Date And Time: {aeg.day:02}/{aeg.month:02}/{aeg.year} {aeg.hour}:{aeg.minute:02} \n")
    f.write(f"Temperature: {get['current']['temperature_2m']}C° \n")
    f.write(f"Humidity: {get['current']['relative_humidity_2m']}% \n")
    f.write(f"Wind Speed: {get['current']['wind_speed_10m']}m/s")
    f.close()