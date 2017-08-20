# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 17:51:05 2016

@author: Vijay
"""

import json
#import urllib
from urlparse import urlparse
import httplib2 as http #External library
import pypyodbc
#import csv
from time import strftime, localtime
from timeit import default_timer
import time




if __name__=="__main__":
    #Authentication parameters
    headers = { 'AccountKey' : 'yBodblIdT3GQGgQjgpj1Cg==',
                'accept' : 'application/json'} #this is by default

    connection = pypyodbc.connect('Driver={SQL Server};'
                                'Server=DESKTOP-K0UG3SE;'
                                'Database=LTADatabase;'
                                )
    cursor = connection.cursor()
    SQLCommand = ("INSERT INTO TravelTimes"
                 "(CurrentDate, CurrentTime, Name, Direction, FarEndPoint, StartPoint, EndPoint, EstTime) "
                "VALUES (?,?,?,?,?,?,?,?)")
    
        
    
    skip = 0 
    Runs = 0     
        
    #API parameters
    uri = 'http://datamall2.mytransport.sg/' #Resource URL
    path = '/ltaodataservice/EstTravelTimes?'
    start = 0
    TotalRuntimeStart = default_timer()    
    
    while True:
    
        if skip == 0:
            start = default_timer()            
            #Build query string & specify type of API call
            target = urlparse(uri + path)
            print target.geturl()
            method = 'GET'
            body = ''
    
            #Get handle to http
            h = http.Http()
            
            date = strftime("%d-%m-%Y", localtime())
            currenttime = strftime("%H:%M:%S", localtime())
    
            #Obtain results
            response, content = h.request(
            target.geturl(),
            method,
            body,
            headers)
    
            #Parse JSON to print
            jsonObj = json.loads(content)
            #print json.dumps(jsonObj["value"][0]["LinkID"], sort_keys=True, indent=4)
            #print jsonObj["MaximumSpeed"]

            #Save result to file
            with open("EstTravelTimes.json","a") as outfile:
                #Saving jsonObj["d"]
                json.dump(jsonObj["value"], outfile, sort_keys=True, indent=4, ensure_ascii=False)
                #print jsonObj["value"]
            
#            with open("SpeedBandsFinal3.csv", "ab") as archive_file:
#                f = csv.writer(archive_file)
#                f.writerow(["CurrentDate", "CurrentTime", "LinkID", "Location", "MaximumSpeed", "MinimumSpeed", "RoadCategory", "RoadName", "SpeedBand"])
#            
                for jsonObj in jsonObj["value"]:
#                    f.writerow([date,
#                            time,
#                            jsonObj["LinkID"], 
#                            jsonObj["Location"], 
#                            jsonObj["MaximumSpeed"],
#                            jsonObj["MinimumSpeed"], 
#                            jsonObj["RoadCategory"], 
#                            jsonObj["RoadName"], 
#                            jsonObj["SpeedBand"]])
                    Values = [date,currenttime,jsonObj["Name"],jsonObj["Direction"],jsonObj["FarEndPoint"],jsonObj["StartPoint"],jsonObj["EndPoint"],jsonObj["EstTime"]]
                    cursor.execute(SQLCommand,Values)
                    connection.commit()
            skip+=50;    
                
        else:
            skipString = "$skip="+str(skip)
            path2 = path+skipString
            
            #Build query string & specify type of API call
            target = urlparse(uri + path2)
            print target.geturl()
            method = 'GET'
            body = ''
    
            #Get handle to http
            h = http.Http()
            date = strftime("%d-%m-%Y", localtime())
            currenttime = strftime("%H:%M:%S", localtime()) 
    
            #Obtain results
            response, content = h.request(
            target.geturl(),
            method,
            body,
            headers)
    
            #Parse JSON to print
            jsonObj = json.loads(content)
            #print json.dumps(jsonObj["value"][0]["LinkID"], sort_keys=True, indent=4)
            #print jsonObj["MaximumSpeed"]
            if jsonObj["value"]:
                #Save result to file
                with open("EstTravelTimes.json","a") as outfile:
                    #Saving jsonObj["d"]
                    json.dump(jsonObj["value"], outfile, sort_keys=True, indent=4, ensure_ascii=False)
                    #print jsonObj["value"]
                
#                with open("SpeedBandsFinal3.csv", "ab") as archive_file:
#                    f = csv.writer(archive_file)
#                    
                
                    for jsonObj in jsonObj["value"]:
#                        f.writerow([date,
#                            time,      
#                            jsonObj["LinkID"], 
#                            jsonObj["Location"], 
#                            jsonObj["MaximumSpeed"],
#                            jsonObj["MinimumSpeed"], 
#                            jsonObj["RoadCategory"], 
#                            jsonObj["RoadName"], 
#                            jsonObj["SpeedBand"]])
                        Values = [date,currenttime,jsonObj["Name"],jsonObj["Direction"],jsonObj["FarEndPoint"],jsonObj["StartPoint"],jsonObj["EndPoint"],jsonObj["EstTime"]]
                        cursor.execute(SQLCommand,Values)
                        connection.commit()
                    
                skip+=50;
            else:
                Runs+=1                
                print "done"+str(Runs)
                duration = default_timer() - start
                TotalRuntime = default_timer() - TotalRuntimeStart
                if TotalRuntime <  43200:
                        
                    time.sleep(120-duration)                
                    skip = 0
                else:
                    print "Complete"                    
                    break
