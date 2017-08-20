# Code to pullout real time weather data from open weather maps.

# Importing required libraries
import urllib
import json
from time import strftime, localtime
from timeit import default_timer
import time
import csv

# Initiating the timer
TotalRuntimeStart = default_timer()

while True:
    
    date = strftime("%d-%m-%Y", localtime())
    currenttime = strftime("%H:%M:%S", localtime())
					
	# Querying the API
    weather = urllib.urlopen('http://api.openweathermap.org/data/2.5/weather?q=Singapore&APPID=98ba6c30b50c8adde17477f5d080fd3a')
    wjson = weather.read()
    wjdata = json.loads(wjson)

    main = wjdata['weather'][0]['main']
    description = wjdata['weather'][0]['description']
    clouds = wjdata['clouds']['all']
    temp = wjdata['main']['temp']
    win_speed = wjdata['wind']['speed']

    try:
        rain = wjdata['rain']['3h']
    except:
        rain = "NA"
	
	# Writing the results to a CSV file
    with open("CurrentWeatherSingapore.csv", "ab") as archive_file:
        f = csv.writer(archive_file)
        f.writerow([date, currenttime, main,description,clouds,temp,win_speed,rain])

    print(currenttime)

    time.sleep(118)