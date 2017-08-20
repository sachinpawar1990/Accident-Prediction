# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 17:51:05 2016

@author: Vijay
"""

import json
import pypyodbc
#import urllib
from urlparse import urlparse
#import pymssql
#import csv
import httplib2 as http #External library
from time import strftime, localtime
import time
from timeit import default_timer


if __name__=="__main__":
    #Authentication parameters
    headers = { 'AccountKey' : 'yBodblIdT3GQGgQjgpj1Cg==',
                'accept' : 'application/json'} #this is by default
    
    
    connection = pypyodbc.connect('Driver={SQL Server};'
                                'Server=localhost;'
                                'Database=LTADatabase;'
                                )
    cursor = connection.cursor()
    SQLCommand = ("INSERT INTO ERPRates"
                 "(EffectiveDate, CurrentDate, CurrentTime, ZoneID, DayType, VehicleType, StartTime, EndTime, ChargeAmount) "
                "VALUES (?,?,?,?,?,?,?,?,?)")

    skip = 0
    Runs = 0
    
    #API parameters
    uri = 'http://datamall2.mytransport.sg/' #Resource URL
    path = '/ltaodataservice/ERPRates?'
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
            with open("ERPRatesTotal2.json","ab") as outfile:
                #Saving jsonObj["d"]
                json.dump(jsonObj["value"], outfile, sort_keys=True, indent=4, ensure_ascii=False)
                #print jsonObj["value"]
            
#            with open("ERPRatesFinal2.csv", "ab") as archive_file:
#                f = csv.writer(archive_file)
#                f.writerow(["EffectiveDate", "CurrentDate", "CurrentTime", "ZoneID", "DayType", "VehicleType", "StartTime", "EndTime", "ChargeAmount"])
                        
                for jsonObj in jsonObj["value"]:
#                    f.writerow([jsonObj["EffectiveDate"],
#                        date,
#                        time,
#                        jsonObj["ZoneID"], 
#                        jsonObj["DayType"],
#                        jsonObj["VehicleType"], 
#                        jsonObj["StartTime"], 
#                        jsonObj["EndTime"], 
#                        jsonObj["ChargeAmount"]])
                    Values = [jsonObj["EffectiveDate"],date,currenttime,jsonObj["ZoneID"], jsonObj["DayType"],jsonObj["VehicleType"],jsonObj["StartTime"],jsonObj["EndTime"],jsonObj["ChargeAmount"]]
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
                with open("ERPRatesTotal2.json","ab") as outfile:
                    #Saving jsonObj["d"]
                    json.dump(jsonObj["value"], outfile, sort_keys=True, indent=4, ensure_ascii=False)
                    #print jsonObj["value"]
                    
#                with open("ERPRatesFinal2.csv", "ab") as archive_file:
#                    
#                    f = csv.writer(archive_file)
                    
                    for jsonObj in jsonObj["value"]:
                        #f.writerow([jsonObj["EffectiveDate"], 
                        #    date,
                        #    time,
                        #    jsonObj["ZoneID"], 
                        #    jsonObj["DayType"],
                        #    jsonObj["VehicleType"], 
                        #    jsonObj["StartTime"], 
                        #    jsonObj["EndTime"], 
                        #    jsonObj["ChargeAmount"]])
                        Values = [jsonObj["EffectiveDate"],date,currenttime,jsonObj["ZoneID"], jsonObj["DayType"],jsonObj["VehicleType"],jsonObj["StartTime"],jsonObj["EndTime"],jsonObj["ChargeAmount"]]
                        cursor.execute(SQLCommand,Values)
                        connection.commit()
                
                skip+=50;
            else:
                Runs+=1                
                print "done"+str(Runs)
                duration = default_timer() - start
                TotalRuntime = default_timer() - TotalRuntimeStart
                if TotalRuntime <  21600:
                        
                    time.sleep(600-duration)                
                    skip = 0
                else:
                    print "Complete" 
                    connection.close()
                    break