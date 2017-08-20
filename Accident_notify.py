import json
from urlparse import urlparse
import httplib2 as http #External library
from time import strftime, localtime
from timeit import default_timer
import time
import datetime
import googlemaps
import folium
import csv
import numpy
import pandas as pd
import webbrowser

from googleplaces import GooglePlaces, types, lang

google_places = GooglePlaces('AIzaSyC8g_X8QgaMPkiaOdLysIRoLRXD49D9PiI')
gmaps = googlemaps.Client(key='AIzaSyC8g_X8QgaMPkiaOdLysIRoLRXD49D9PiI')
currenttime = strftime("%H:%M:%S", localtime())

html="""
<!DOCTYPE html>
<html>
<head>
<!-- Styles -->	
<style style="text/css">
.blink_me {
  -moz-animation: blinker 1s linear infinite;
  -webkit-animation: blinker 1s linear infinite;
  animation: blinker 1s linear infinite;
}

@keyframes blinker {  
  50% { opacity: 0.0; }
}

@-webkit-keyframes blinker {  
  50% { opacity: 0.0; }
}

@-moz-keyframes blinker {  
  50% { opacity: 0.0; }
}
</style>
</head>
<body style="background:white">
    <div style="background:white;color:black;height:20px;">
        <p class="blink_me" style="text-align:center;font-size:8px;vertical-align:middle;padding-top:5px">RECEIVING ALERT</p>
    </div>	
</body>
</html>
"""

if __name__=="__main__":
    #Authentication parameters
    headers = { 'AccountKey' : 'yBodblIdT3GQGgQjgpj1Cg==',
                'accept' : 'application/json'} #this is by default
                
    #API parameters
    uri = 'http://datamall2.mytransport.sg/' #Resource URL
    path = '/ltaodataservice/TrafficIncidents?'
    start = 0
    TotalRuntimeStart = default_timer() 
    
    #Build query string & specify type of API call
    target = urlparse(uri + path)
    #print target.geturl()
    method = 'GET'
    body = ''
    #Get handle to http
    h = http.Http()
    #Obtain results
    response, content = h.request(
    target.geturl(),
    method,
    body,
    headers)
    #Parse JSON to print
    jsonObj = json.loads(content)
    
    # Defining the map    
    map_1 = folium.Map(location=[1.32853669914, 103.846601732], zoom_start=12)                
    
    for jsonObj in jsonObj["value"]:
        if jsonObj["Type"]=="Accident":
            dttime = json.dumps(jsonObj["Message"], sort_keys=True, indent=4)
            words = dttime.split()

            mytime = words[0]   
            onlytimeList = mytime.split(")")
            onlytime = onlytimeList[1]+":00"
            
            #print onlytime
            difference = datetime.datetime.strptime(currenttime,'%H:%M:%S') - datetime.datetime.strptime(onlytime,'%H:%M:%S')
            diff_second = abs(difference.total_seconds())
            
            if (diff_second < 1200):
                #print (jsonObj["Latitude"],jsonObj["Longitude"])
                lat=jsonObj["Latitude"]
                long=jsonObj["Longitude"]
                reverse_geocode_result = gmaps.reverse_geocode((lat, long))
                toDisplay = ( jsonObj["Type"] + " at " + reverse_geocode_result[0]['address_components'][0]['long_name'])
                print toDisplay                
                                
                query_result = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=500, types=[types.TYPE_HOSPITAL])
                if len(query_result.places)==0:
                    query_result = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=5000, types=[types.TYPE_HOSPITAL])
                
                time.sleep(1)
                
                query_result2 = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=500, types=[types.TYPE_FIRE_STATION])
                if len(query_result2.places)==0:
                    query_result2 = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=5000, types=[types.TYPE_FIRE_STATION])
                
                time.sleep(1)
                
                query_result3 = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=500, types=[types.TYPE_POLICE])
                if len(query_result3.places)==0:
                    query_result3 = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=5000, types=[types.TYPE_POLICE])                
                
                time.sleep(1)
                msg1 = jsonObj["Message"].split(".",1)
                msg2 = str(msg1[0].split(" ",1)[1])
                #print ("Message : " + msg2)
                
                #print ("Nearest Hospital at : " + query_result.places[0].name)
                query_result.places[0].get_details()
                time.sleep(1)
                #print ("Hospital Contact No. :" + query_result.places[0].local_phone_number)
                #print ("Nearest Fire-Station at : " + query_result2.places[0].name)
                query_result2.places[0].get_details()
                time.sleep(1)
                #print ("Fire-Station Contact No. :" + query_result2.places[0].local_phone_number)
                #print ("Nearest Police-Post at : " + query_result3.places[0].name)
                query_result3.places[0].get_details()
                #print ("Police-Post Contact No.: " + str(query_result3.places[0].local_phone_number))
                
                time.sleep(1)
                
                q1lat = float(query_result.places[0].geo_location['lat'])
                q1long = float(query_result.places[0].geo_location['lng'])
                
                q2lat = float(query_result2.places[0].geo_location['lat'])
                q2long = float(query_result2.places[0].geo_location['lng'])
                
                q3lat = float(query_result3.places[0].geo_location['lat'])
                q3long = float(query_result3.places[0].geo_location['lng'])
                
                #plotting on graph
                iframe = folium.element.IFrame(html=html, width=100, height=40)
                popup = folium.Popup(iframe, max_width=2650)
                popup2 = folium.Popup(iframe, max_width=2650)
                popup3 = folium.Popup(iframe, max_width=2650)
                folium.Marker([lat, long], popup=toDisplay,
                                   icon = folium.Icon(color ='orange', icon = 'warning-sign')).add_to(map_1)
                folium.Marker([q1lat, q1long], popup=popup,
                                   icon = folium.Icon(color ='green', icon = 'heart')).add_to(map_1)
                folium.Marker([q2lat, q2long], popup=popup2,
                                   icon = folium.Icon(color ='red', icon = 'fire')).add_to(map_1)
                folium.Marker([q3lat, q3long], popup=popup3,
                                   icon = folium.Icon(color ='blue', icon = 'user')).add_to(map_1)
                my_PolyLine1=folium.PolyLine(locations=[[lat,long],[q1lat, q1long]],weight=5, color='#EE7600')
                map_1.add_children(my_PolyLine1)
                my_PolyLine2=folium.PolyLine(locations=[[lat,long],[q2lat, q2long]],weight=5, color='#EE7600')
                map_1.add_children(my_PolyLine2)
                my_PolyLine3=folium.PolyLine(locations=[[lat,long],[q3lat, q3long]],weight=5, color='#EE7600')
                map_1.add_children(my_PolyLine3)
                
        elif jsonObj["Type"]=="Vehicle breakdown":
            dttime = json.dumps(jsonObj["Message"], sort_keys=True, indent=4)
            words = dttime.split()
            
            mytime = words[0]   
            onlytimeList = mytime.split(")")
            onlytime = onlytimeList[1]+":00"
            
            #print onlytime
            difference = datetime.datetime.strptime(currenttime,'%H:%M:%S') - datetime.datetime.strptime(onlytime,'%H:%M:%S')
            diff_second = abs(difference.total_seconds())
            if (diff_second < 1200):
                #print (jsonObj["Latitude"],jsonObj["Longitude"])
                lat=jsonObj["Latitude"]
                long=jsonObj["Longitude"]
                reverse_geocode_result = gmaps.reverse_geocode((lat, long))
                toDisplay = ( jsonObj["Type"] + " at " + reverse_geocode_result[0]['address_components'][0]['long_name'])
                print toDisplay                
                
                query_result2 = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=500, types=[types.TYPE_CAR_REPAIR])
                if len(query_result2.places)==0:
                    query_result2 = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=5000, types=[types.TYPE_CAR_REPAIR])
                
                time.sleep(1)
                
                query_result3 = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=500, types=[types.TYPE_POLICE])
                if len(query_result3.places)==0:
                    query_result3 = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=5000, types=[types.TYPE_POLICE])                
                
                msg1 = jsonObj["Message"].split(".",1)
                msg2 = str(msg1[0].split(" ",1)[1])
                #print ("Message : " + msg2)                
                
                #print ("Nearest Fire-Station at : " + query_result2.places[0].name)
                query_result2.places[0].get_details()
                time.sleep(1)
                #print ("Fire-Station Contact No. :" + query_result2.places[0].local_phone_number)
                #print ("Nearest Police-Post at : " + query_result3.places[0].name)
                query_result3.places[0].get_details()
                #print ("Police-Post Contact No.: " + str(query_result3.places[0].local_phone_number))
                
                time.sleep(1)
                
                q2lat = float(query_result2.places[0].geo_location['lat'])
                q2long = float(query_result2.places[0].geo_location['lng'])
                
                q3lat = float(query_result3.places[0].geo_location['lat'])
                q3long = float(query_result3.places[0].geo_location['lng'])
                
                #plotting on graph
                iframe = folium.element.IFrame(html=html, width=100, height=40)
                popup2 = folium.Popup(iframe, max_width=2650)
                popup3 = folium.Popup(iframe, max_width=2650)
                folium.Marker([lat, long], popup=toDisplay,
                                   icon = folium.Icon(color ='orange', icon = 'warning-sign')).add_to(map_1)
                folium.Marker([q2lat, q2long], popup=popup2,
                                   icon = folium.Icon(color ='pink', icon = 'road')).add_to(map_1)
                folium.Marker([q3lat, q3long], popup=popup3,
                                   icon = folium.Icon(color ='blue', icon = 'user')).add_to(map_1)
                my_PolyLine2=folium.PolyLine(locations=[[lat,long],[q2lat, q2long]],weight=5, color='#EE7600')
                map_1.add_children(my_PolyLine2)
                my_PolyLine3=folium.PolyLine(locations=[[lat,long],[q3lat, q3long]],weight=5, color='#EE7600')
                map_1.add_children(my_PolyLine3)
                
        elif jsonObj["Type"]=="Unattended Vehicle":
            dttime = json.dumps(jsonObj["Message"], sort_keys=True, indent=4)
            words = dttime.split()
            
            mytime = words[0]   
            onlytimeList = mytime.split(")")
            onlytime = onlytimeList[1]+":00"
            
            #print onlytime
            difference = datetime.datetime.strptime(currenttime,'%H:%M:%S') - datetime.datetime.strptime(onlytime,'%H:%M:%S')
            diff_second = abs(difference.total_seconds())
            if (diff_second < 1200):
                #print (jsonObj["Latitude"],jsonObj["Longitude"])
                lat=jsonObj["Latitude"]
                long=jsonObj["Longitude"]
                reverse_geocode_result = gmaps.reverse_geocode((lat, long))
                toDisplay = ( jsonObj["Type"] + " at " + reverse_geocode_result[0]['address_components'][0]['long_name'])
                print toDisplay                
                
                query_result3 = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=500, types=[types.TYPE_POLICE])
                if len(query_result3.places)==0:
                    query_result3 = google_places.nearby_search(lat_lng={'lat':lat,'lng':long},radius=5000, types=[types.TYPE_POLICE])                
                
                msg1 = jsonObj["Message"].split(".",1)
                msg2 = str(msg1[0].split(" ",1)[1])
                #print ("Message : " + msg2)                
                
                #print ("Nearest Police-Post at : " + query_result3.places[0].name)
                query_result3.places[0].get_details()
                #print ("Police-Post Contact No.: " + str(query_result3.places[0].local_phone_number))
                
                time.sleep(1)
                
                q3lat = float(query_result3.places[0].geo_location['lat'])
                q3long = float(query_result3.places[0].geo_location['lng'])
                
                #plotting on graph
                iframe = folium.element.IFrame(html=html, width=100, height=40)
                popup3 = folium.Popup(iframe, max_width=2650)
                folium.Marker([lat, long], popup=toDisplay,
                                   icon = folium.Icon(color ='orange', icon = 'warning-sign')).add_to(map_1)
                folium.Marker([q3lat, q3long], popup=popup3,
                                   icon = folium.Icon(color ='blue', icon = 'user')).add_to(map_1)
                my_PolyLine3=folium.PolyLine(locations=[[lat,long],[q3lat, q3long]],weight=5, color='#EE7600')
                map_1.add_children(my_PolyLine3)
                
map_1.save('showAllEvents.html')

url = 'showAllEvents.html'
webbrowser.open_new_tab(url)         