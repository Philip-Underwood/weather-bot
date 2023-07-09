import json
import sys
from urllib.request import urlopen
from Discord import Discord

TempYesterdayFilepath = __file__[:-len("Morning.py")] + "TempYesterday.txt"


def GetForecast():
    URL = "https://api.weather.gov/points/38.9162,-94.7066"
    try:
        Response = urlopen(URL)
    except Exception:
        print("ERROR: No response from weather.gov API")
        sys.exit
    Data = json.loads(Response.read())

    ForecastURL = Data['properties']['forecast']
    try:
        Response = urlopen(ForecastURL)
    except Exception:
        print("ERROR: No response from weather.gov API")
        sys.exit
    Data = json.loads(Response.read())

    return Data


def GetTemp(Data):
    periods = Data['properties']['periods']
    return periods[0]['temperature']


def GetTempYesterday():
    try:
        TempYesterdayFile = open(TempYesterdayFilepath, "r")
        TempYesterday = TempYesterdayFile.read()
        TempYesterdayFile.close()
        return TempYesterday
    except Exception as e:
        print("ERROR: exception raised:" + e)
        return "70"


def GetStatus(TempToday, TempYesterday):
    TempT = int(TempToday)
    TempY = int(TempYesterday)
    StatusT = ""
    StatusY = ""

    match TempT:
        case num if 65 <= num <= 75:
            StatusT = "nice"
            EmojiT = ":leaves:"
        case num if num < 65:
            StatusT = "cold"
            EmojiT = ":snowflake:"
        case num if num > 75:
            StatusT = "hot"
            EmojiT = ":sunny:"
        case num if num > 88:
            StatusT = "very hot"
            EmojiT = ":fire:"

    match TempY:
        case num if 65 <= num <= 75:
            StatusY = "nice"
            EmojiY = ":leaves:"
        case num if num < 65:
            StatusY = "cold"
            EmojiY = ":snowflake:"
        case num if num > 75:
            StatusY = "hot"
            EmojiY = ":sunny:"
        case num if num > 88:
            StatusY = "very hot"
            EmojiY = ":fire:"

    return StatusT, StatusY, EmojiT, EmojiY


def CompareTemp(StatusT, StatusY, EmojiT, EmojiY, TempT, TempY):
    if StatusT != StatusY:
        return "Today's weather is changing from " + EmojiY + " " + StatusY + " (" + \
               str(TempY) + "°F) to " + EmojiT + " " + StatusT + " (" + str(TempT) + "°F)."
    else:
        return "null"


def RecordTemp(TempToday):
    try:
        TempYesterdayFile = open(TempYesterdayFilepath, "w")
        TempYesterdayFile.write(str(TempToday))
        TempYesterdayFile.close()
    except Exception:
        print("ERROR: Could not write to TempYesterday file")


print("Checking Morning Forecast...")
Data = GetForecast()
TempToday = GetTemp(Data)
TempYesterday = GetTempYesterday()

StatusT, StatusY, EmojiT, EmojiY = GetStatus(TempToday, TempYesterday)
CompareTempMsg = CompareTemp(StatusT, StatusY, EmojiT, EmojiY, TempToday, TempYesterday)
if CompareTempMsg != "null":
    Discord(CompareTempMsg)
    print("Morning Forecast Sent")
else:
    print("Morning Forecast Not Sent")

RecordTemp(TempToday)
