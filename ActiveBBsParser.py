# This file is for messing with the way activeBBs.txt is parsed, without screwing up UsefulFunctions_PAG.py

import UsefulFunctions as uf
from UsefulFunctions import Earthquake
import numpy as np
import re
import pandas as pd
#
eq = Earthquake('Data/grid.xml')
# print(eq.detection_time)

# Create an array from activeBBs.txt, specify data types and names for each column, delimit based on fixed char lengths
# ActiveBBs = np.genfromtxt('Data/activeBBs.txt',
#                           delimiter=[8, 9, 12, 8, 50],
#                           dtype=[('sta', 'U5'), ('lat', 'f8'), ('lon', 'f8'), ('elev', 'f8'), ('staname', 'U50')],
#                           autostrip=True,
#                           )
# for i in ActiveBBs['elev']:
#     print(i)
#
# print(ActiveBBs.shape)

# Azimuth calculation and Azimuthal Gap
# sta_dist = np.array(
#     [uf.getDistance(lat, lon, i, k)
#      for (i, k) in zip(Earthquake.ActiveBBs['lat'], Earthquake.ActiveBBs['lon'])]
# )
# sta_dist = np.array(
#     np.sqrt(np.power(sta_dist, 2) + depth**2)
# )
# # Calculate P wave travel time to each station
# station_arrivals_p = sta_dist / vp
# n = 0  # Increasing number of stations
# gap = 360  # Azimuthal Gap tacker
# while gap >=120 or
#     stats = Earthquake.ActiveBBs
# lights_on = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# lights_on = np.vstack((lights_on[-1,:], lights_on, lights_on[0,:]))
# print(lights_on)
# bearings = np.array([10, 50, 60, 180, 299])
# bearings = np.hstack((bearings[-1], bearings, bearings[0]))
# # bearings = np.insert(bearings, 0, bearings[-1])
# # bearings = np.append(bearings, -1, bearings[1])
# print(bearings)

# Change from .txt to .csv files
# ActiveBBs = np.genfromtxt('Data/station_list.csv')
stations_kept = pd.read_csv('Data/stations_Kept.csv', quotechar='"')
print(stations_kept['lat'])
print(stations_kept['lat'][0] + stations_kept['lat'][1])
