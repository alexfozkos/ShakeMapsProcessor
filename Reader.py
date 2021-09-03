# This should read an XML file from ShakeMaps, grab the lat/lon measurements and intensity data for the data points,
# and make it 'workable', for testing, using this earthquake https://earthquake.alaska.edu/event/0219dg4uxz/shakemap/download
import xml.etree.ElementTree as ET
import math
import numpy as np
from matplotlib import pyplot as plt

# read in the xml
tree = ET.parse('grid.xml')
root = tree.getroot()
# elat = root[]

# ~~~~DEBUG~~~~
# print(root.attrib)
for child in root:
    print(child.tag, child.attrib)
# print (root[-1].attrib)
# ~~~~DEBUG~~~~

elat = float(root[0].attrib['lat'])
elon = float(root[0].attrib['lon'])

# grab last node in the root, I assume that is always grid_data, and split it by \n to get each data point. Then, save
# as a list and pop the first and last empty \n's
# Can add substring [:x] to the end of this for quicker testing
gridDataList = root[-1].text.split("\n")
if gridDataList[0] == '':
    gridDataList.pop(0)
if gridDataList[-1] == '':
    gridDataList.pop(-1)
# print(gridDataList)

# make a while loop to store each data point (each item in gridDataList) in a dictionary (gridDataDict) as a list itself
# this gives us a dictionary of points, each containing grabbable index info (remember index 1 is [0], 2 is [1], etc...)
# This could be fixed by adding a null item at the start of every point? Maybe worthwhile for simpler readability?
# <grid_field index="1" name="LON" units="dd"/> lon
# <grid_field index="2" name="LAT" units="dd"/> lat
# <grid_field index="3" name="MMI" units="intensity"/> modified mercalli intensity?
# <grid_field index="4" name="PGA" units="%g"/> peak ground acceleration
# <grid_field index="5" name="PGV" units="cm/s"/> peak ground velocity
# <grid_field index="6" name="PSA03" units="%g"/> ?
# <grid_field index="7" name="PSA10" units="%g"/> ?
# <grid_field index="8" name="PSA30" units="%g"/> ?
# <grid_field index="9" name="SVEL" units="m/s"/> ?

gridDataDict = {}
i = 0
while i < len(gridDataList):
    gridDataDict[i] = gridDataList[i].split(" ")
    i += 1
# for v in gridDataDict.values():
#     print(v)
print(len(gridDataDict))


# function for calculating great circle distance between two lat lon points using haversine formula
# https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula


def getDistance(lat1, lon1, lat2, lon2):
    r = 6371  # Radius of earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)) ** 2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon / 2)) ** 2
    a = math.fabs(a)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = r * c  # distance in km
    return d

# turns data dictionary into a dictionary of distance keys and PGA values, which can then be ordered by key(distance)(x)
# and plotted as a scatter plot


distanceVsPGADict = {}

for k, v in gridDataDict.items():
    distanceVsPGADict[getDistance(elat, elon, float(v[1]), float(v[0]))] = float(v[3])
    # print(v[1], v[0], getDistance(elat, elon, float(v[1]), float(v[0])), float(v[3]))

distanceVsPGAxy = sorted(distanceVsPGADict.items())
x1, y1 = zip(*distanceVsPGAxy)

plt.scatter(x1, y1)
plt.xlabel('Distance (km)')
plt.ylabel('Peak Acceleration (%g)')
plt.show()

# Are the minor exponential trends in the data plot hills/valleys?
# what is that bottom layer of data with very low PGA?
# how do I analyze this?


x2 = np.array([])  # don't do list do dict i think it's faster future me fix this thanks
y2 = np.array([])
pga = np.array([])
for k, v in gridDataDict.items():
    np.append(x2, v[0])
    np.append(y2, v[1])
    np.append(pga, v[3])
print(len(x2))
print(len(y2))
print(len(pga))
plt.scatter(x2, y2, s=pga*100)
plt.xlabel('lon')
plt.ylabel('lat')
plt.show()
