# This should read an XML file from ShakeMaps, grab the lat/lon measurements and intensity data for the data points,
# and make it 'workable', for testing, using this earthquake https://earthquake.alaska.edu/event/0219dg4uxz/shakemap/download
import xml.etree.ElementTree as ET
import math
import numpy as np
from matplotlib import pyplot as plt

# read in the xml
tree = ET.parse('grid.xml')
root = tree.getroot()

# grab event coords and grid size
elat = float(root[0].attrib['lat'])
elon = float(root[0].attrib['lon'])
nlat = int(root[1].attrib['nlat'])
nlon = int(root[1].attrib['nlon'])

# turn big data string into a nice array
gridDataArray = np.array(root[-1].text.replace('\n', ' ').split(' ')[1:-1], dtype=float)
gridDataArray = np.reshape(gridDataArray, (int(nlat*nlon), 9))

# Each column of the array is defined here, each row is a data point
# <grid_field index="1" name="LON" units="dd"/> lon
# <grid_field index="2" name="LAT" units="dd"/> lat
# <grid_field index="3" name="MMI" units="intensity"/> modified mercalli intensity?
# <grid_field index="4" name="PGA" units="%g"/> peak ground acceleration
# <grid_field index="5" name="PGV" units="cm/s"/> peak ground velocity
# <grid_field index="6" name="PSA03" units="%g"/> ?
# <grid_field index="7" name="PSA10" units="%g"/> ?
# <grid_field index="8" name="PSA30" units="%g"/> ?
# <grid_field index="9" name="SVEL" units="m/s"/> ?


# function for calculating great circle distance between two lat lon points using haversine formula
# https://community.esri.com/t5/coordinate-reference-systems-blog/distance-on-a-sphere-the-haversine-formula/ba-p/902128
def getDistance(lat1, lon1, lat2, lon2):
    r = 6371  # Radius of earth in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2)) ** 2 + math.cos(phi1) * math.cos(phi2) * (math.sin(dlambda / 2)) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = r * c  # distance in km
    return d


lats = gridDataArray[:, 1]
lons = gridDataArray[:, 0]
pga = gridDataArray[:, 3]
distance = np.array([getDistance(elat, elon, i, k) for (i, k) in zip(lats, lons)])

plt.scatter(distance, pga, s=0.3)
plt.xlabel('Distance (km)')
plt.ylabel('Peak Acceleration (%g)')
plt.savefig('PGA-vs-Distance.png')


plt.clf()

# making a plot of arrival times vs distance
# can change this to take into account depth by adding if statement and checking depth from grid.xml
vp = 6.2
vs = vp * .6
vsurf = vs * .9

arrivalP = distance/vp
arrivalS = distance/vs
arrivalSurf = distance/vsurf

plt.plot(distance, arrivalP, 'g', label='P Arrivals')
plt.plot(distance, arrivalS, 'y', label='S Arrivals')
plt.plot(distance, arrivalSurf, 'r', label='Surface Arrivals')
plt.plot(distance, arrivalSurf-arrivalP, 'm', label='P-Surface Lag')
plt.xlabel('Distance (km)')
plt.ylabel('Time (s)')
plt.legend()
plt.savefig('Arrival-Times.png')


plt.clf()

# combining the above 2 plots into 1 image and zooming into the intersection a little bit
fig, ax1 = plt.subplots()
ax1.set_xlabel('PGA (%g)')
ax1.set_ylabel('Distance (km)', color='b')
ax1.scatter(distance, pga, s=0.2)
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_xlim(0, 100)  # Zooms into the first section of the graph

ax2 = ax1.twinx()  # Creates a clone that shares the x axis, new y axis is put on other side

ax2.set_ylabel('Time (s)', color='k')
ax2.plot(distance, arrivalP, 'g', label='P Arrivals')
ax2.plot(distance, arrivalS, 'y', label='S Arrivals')
ax2.plot(distance, arrivalSurf, 'r', label='Surface Arrivals')
ax2.plot(distance, arrivalSurf-arrivalP, 'm', label='P-Surface Lag')
ax2.tick_params(axis='y', labelcolor='k')
ax2.legend()

fig.tight_layout()
plt.savefig('PGA-Times-Distance.png')
