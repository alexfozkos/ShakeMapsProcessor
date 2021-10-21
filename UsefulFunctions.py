import xml.etree.ElementTree as ET
import math
import numpy as np
import requests


# downloads grid.xml from shakemaps url because I can't figure out how to download it otherwise
def download(url):
    response = requests.get(url)
    with open('grid.xml', 'wb') as file:
        file.write(response.content)


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


class Earthquake:
    count = 0

    # travel time engine
    # wave velocities (km/s)
    vel_p = 6.7
    vel_s = vel_p * 0.6
    vel_surf = vel_s * 0.9
    # detection engine
    # time to process earthquake (s)
    ttp = 12

    # default init takes a string, assumes that the string is the name of a shakemap xml grid file,
    # defaults to 'grid.xml'
    def __init__(self, xml='grid.xml'):
        # shake engine
        # parse an xml file using a name of a grid.xml
        self.tree = ET.parse(xml)
        self.root = self.tree.getroot()

        # event info
        self.event_id = str(self.root[0].attrib['event_id'])
        self.event_lat = float(self.root[0].attrib['lat'])
        self.event_lon = float(self.root[0].attrib['lon'])
        self.event_magnitude = float(self.root[0].attrib['magnitude'])
        self.event_depth = float(self.root[0].attrib['depth'])
        self.event_timestamp = str(self.root[0].attrib['event_timestamp'])
        self.event_network = str(self.root[0].attrib['event_network'])
        self.event_description = str(self.root[0].attrib['event_description'])
        self.event_intensity_observations = int(self.root[0].attrib['intensity_observations'])

        # grid specs
        self.nlat = int(self.root[1].attrib['nlat'])
        self.nlon = int(self.root[1].attrib['nlon'])
        self.lon_min = float(self.root[1].attrib['lon_min'])
        self.lon_max = float(self.root[1].attrib['lon_max'])
        self.lat_min = float(self.root[1].attrib['lat_min'])
        self.lat_max = float(self.root[1].attrib['lat_max'])

        # grid data array
        gridarray = np.array(self.root[-1].text.replace('\n', ' ').split(' ')[1:-1], dtype=float)
        gridarray = np.reshape(gridarray, (int(self.nlat * self.nlon), 9))
        self.lons = np.array([gridarray[:, 0]]).T
        self.lats = np.array([gridarray[:, 1]]).T
        self.mmi = np.array([gridarray[:, 2]]).T
        self.pga = np.array([gridarray[:, 3]]).T
        self.pgv = np.array([gridarray[:, 4]]).T
        self.psa03 = np.array([gridarray[:, 5]]).T
        self.psa10 = np.array([gridarray[:, 6]]).T
        self.psa30 = np.array([gridarray[:, 7]]).T
        self.svel = np.array([gridarray[:, 8]]).T

        # create distances and travel times for each point
        self.distances = np.array(
            [[getDistance(self.event_lat, self.event_lon, i, k) for (i, k) in zip(self.lats, self.lons)]]
        ).T
        self.arrivals_s = self.distances/Earthquake.vel_s
        self.warning_times = self.arrivals_s - Earthquake.ttp
        # this next line makes negative warning times 0
        # self.warning_times = np.where(self.warning_times < 0, 0, self.warning_times)

        Earthquake.count += 1
