from obspy.clients.fdsn import Client
from obspy import UTCDateTime
client = Client("IRIS")
from obspy.clients.fdsn.header import FDSNNoDataException
from obspy import Stream
from obspy import Trace
from obspy import read, read_inventory
from obspy.signal.filter import envelope
from obspy import read_inventory
import numpy as np
import pandas as pd
import time
import os
####################################################################################################################################################################################
#makestalist
#This is an informal script to aid in the creation of sta_file. Unlike the other programs, this is a script with hardwired values that users are likely to manipulate directly in order to assemble the specific set of stations they want. 
####################################################################################################################################################################################
def makestalist(network,station,channel,location,datetime):
    start_time = time.time()
    df =  pd.DataFrame(columns = ['network','station','channel','location','latitude','longitude','elevation'])
    starttime = UTCDateTime(datetime)  
    inv = client.get_stations(network=network,station=station,channel=channel,location=location,starttime=starttime,level='response')
   # print(inv.response.Response._get_overall_sensitivity_and_gain)
    noi = len(inv) #number of networks
    nol = len(df) #number of locations in df. this is done to write different network rows properly into dataframe. 
    for i in range(noi):
        net = inv[i]
        netcod = inv[i].code
        print(netcod)
        nos = len(net)  #number of stations in each network
        for s in range(nos):
            stacod=net[s].code 
            stalat=net[s].latitude
            stalon=net[s].longitude
            staelv=net[s].elevation
            chn = net[s] 
            noc = len(chn) #number of channels in each station
            for c in range(noc):
               cha = chn[c].code
               loc = chn[c].location_code
            data = netcod,stacod,cha,loc,stalat,stalon,staelv
            df.loc[s+nol] = data 
        nol = len(df)
    df.append(df, ignore_index = True)        
    print(df)
    print(inv)
    df.to_csv('prep/stafile.csv',index=False)
    inv.write("prep/invfile.xml",format="STATIONXML")
    print("--- %s seconds ---" % (time.time() - start_time))