# Code to get the data in a required format for plotting in Tableau

# Importing libraries
import csv
import pandas as pd

all_exp_data = pd.read_csv("C:/SpeedBandsCatA.csv")

# Getting all the required data from the csv
all_curdate = all_exp_data.CurrentDate
all_curtime = all_exp_data.CurrentTime
all_linkid = all_exp_data.LinkID
all_slat = all_exp_data.startlat
all_slon = all_exp_data.startlon
all_elat = all_exp_data.endlat
all_elon= all_exp_data.endlon
all_rn = all_exp_data.RoadName
all_sb = all_exp_data.SpeedBand
all_cnt = all_exp_data.Count
all_flg = all_exp_data.Flag

# Declaring all variables
currdate = []
currtime = []
linkid = []
lat = []
lon = []
roads = []
sband = []
cnt = []
flaglat = []
flaglon = []


for CurrentDate, CurrentTime,LinkID,startlat,startlon,endlat,endlon,RoadName,SpeedBand,Count,Flag in zip(all_curdate,all_curtime,all_linkid,all_slat,all_slon,all_elat,all_elon,all_rn,all_sb,all_cnt,all_flg):
    # Row 1
    try:
        currdate.append(CurrentDate)
        currtime.append(CurrentTime)
        linkid.append(LinkID)
        lat.append(startlat)
        lon.append(startlon)
        roads.append(RoadName)
        sband.append(SpeedBand)
        cnt.append('0')
        flaglat.append('999999999')
        flaglon.append('999999999')

        # Row 2
        currdate.append(CurrentDate)
        currtime.append(CurrentTime)
        linkid.append(LinkID)
        lat.append(endlat)
        lon.append(endlon)
        roads.append(RoadName)
        sband.append(SpeedBand)
        cnt.append(Count)

        if Flag == 1:
            flaglat.append(endlat)
            flaglon.append(endlon)
        else:
            flaglat.append('999999999')
            flaglon.append('999999999')
            
    except:
        continue

# Writing back to CSV
with open('SpeedBandsCatA_Formatted_Flag.csv','w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(currdate,currtime,linkid,lat,lon,roads,sband,flaglat,flaglon))