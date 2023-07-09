import json
import sys
from urllib.request import urlopen
from Discord import Discord


def GetForecast():
    URL = "https://api.weather.gov/points/38.9162,-94.7066"
    try:
        Response = urlopen(URL)
    except Exception:
        print("ERROR: No response from weather.gov API")
        sys.exit
    Data = json.loads(Response.read())

    ForecastURL = Data['properties']['forecastHourly']
    try:
        Response = urlopen(ForecastURL)
    except Exception:
        print("ERROR: No response from weather.gov API")
        sys.exit
    Data = json.loads(Response.read())

    return Data


def GetTemps(Data):
    periods = Data['properties']['periods']

    Temps = []
    for i in range(0, 7):
        Temps.append(periods[i]['temperature'])

    return Temps


def CheckWindow(Low):
    if Low >= 45 and Low <= 65:
        return True
    else:
        return False


def CheckRain(Data):
    periods = Data['properties']['periods']

    RainChances = []

    for i in range(9, 18):
        RainChances.append(periods[i]['probabilityOfPrecipitation']['value'])

    return max(RainChances)


print("Checking Night Forecast...")
DiscordMsg = ""
Data = GetForecast()
Temps = GetTemps(Data)
CurrentTemp = Temps[0]
Low = min(Temps)
OpenWindow = CheckWindow(Low)

RainChance = CheckRain(Data)

if OpenWindow:
    DiscordMsg = "Open the window! It is " + str(CurrentTemp) + "°F out with a low of "\
                 + str(Low) + "°F."

if RainChance > 50:
    if OpenWindow:
        DiscordMsg += "\n\nAlso, t"
    else:
        DiscordMsg += "T"
    DiscordMsg += "here's a " + str(RainChance) + "% chance of rain tomorrow."

if OpenWindow or RainChance > 50:
    Discord(DiscordMsg)
    print("Night Forecast Sent")
else:
    print("Night Forecast Not Sent")
