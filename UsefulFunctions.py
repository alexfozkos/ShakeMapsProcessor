import xml.etree.ElementTree as ET
import math
import numpy as np
import requests
import os


# downloads grid.xml from shakemaps url because I can't figure out how to download it otherwise
def download(url):
    response = requests.get(url)
    with open('Data/grid.xml', 'wb') as file:
        file.write(response.content)


ActiveBBs = np.genfromtxt('Data/activeBBs.txt',
                          delimiter=[8, 9, 12, 8, 50],
                          # encoding='utf-8',
                          dtype=[('sta', 'U5'), ('lat', 'f8'), ('lon', 'f8'), ('elev', 'f8'), ('staname', 'U50')],
                          # usecols=(0, 1, 2, 3),
                          autostrip=True,
                          )


def calculateDetectionTime(lon, lat, depth, vp):
    sta_dist = np.array(
        [getDistance(lat, lon, i, k)
         for (i, k) in zip(Earthquake.ActiveBBs['lat'], Earthquake.ActiveBBs['lon'])]
    )

    sta_dist = np.array(
        np.sqrt(np.power(sta_dist, 2) + depth**2)
    )
    # sta_dist_col = sta_dist.reshape(sta_dist.shape[0], 1)

    # Calculate P wave travel time to each station
    sta_arr_p = sta_dist / vp
    # sta_arr_p_col = sta_arr_p.reshape(sta_arr_p.shape[0], 1)
    print(Earthquake.ActiveBBs['lon'][:3])
    sta_list = np.vstack((Earthquake.ActiveBBs['lon'], Earthquake.ActiveBBs['lat'], sta_dist, sta_arr_p))
    sta_list = sta_list.transpose()
    sta_list = sta_list[sta_list[:, 3].argsort()]
    n = 0  # Increasing number of stations
    bearings = np.array([])
    gaps = np.array([])
    max_gap = 360  # Azimuthal Gap tacker
    max_dist = 0
    while max_gap >= 120 or max_dist <= 50:
        # The x closest stations, increase by one each time we fail to meet criteria
        lights_on = Earthquake.ActiveBBs[Earthquake.DR + n, :]
        # find bearings
        for i in range(0, Earthquake.DR + n):
            bearings = np.append(bearings, getBearing(lon, lat, lights_on[i, 0], lights_on[i, 1]))
        # sort the bearings in clockwise order
        bearings = np.sort(bearings)
        # add first bearing to end and last bearing to start to pseudo-wrap the bearings
        bearings = np.hstack((bearings[-1], bearings, bearings[0]))
        # find gaps between each bearing
        for i in range(1, Earthquake.DR + n + 1):
            gaps = np.append(gaps, )


    detection_time = np.sort(sta_arr_p)[Earthquake.DR - 1]

    return detection_time


# function for finding the bearing between two points
# https://towardsdatascience.com/calculating-the-bearing-between-two-geospatial-coordinates-66203f57e4b4
def getBearing(lon1, lat1, lon2, lat2):
    a = {'lat': lat1, 'lon': lon1}  # epicenter
    b = {'lat': lat2, 'lon': lon2}  # station
    dL = b.lon - a.lon
    X = np.cos(b.lat) * np.sin(dL)
    Y = np.cos(a.lat) * np.sin(b.lat) - np.sin(a.lat) * np.cos(b.lat) * np.cos(dL)
    bearing = np.arctan2(X, Y)
    bearing = (np.degrees(bearing) + 360) % 360
    return bearing

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
    # Create an array containing info for active BB stations, used to calculate detection time
    ActiveBBs = np.genfromtxt('Data/activeBBs.txt',
                              delimiter=[8, 9, 12, 8, 50],
                              # encoding='utf-8',
                              dtype=[('sta', 'U5'), ('lat', 'f8'), ('lon', 'f8'), ('elev', 'f8'), ('staname', 'U50')],
                              # usecols=(0, 1, 2, 3),
                              autostrip=True,
                              )
    count = 0

    # wave velocities (km/s)
    vel_p = 6.7
    vel_s = vel_p * 0.6
    vel_surf = vel_s * 0.9
    # Detection Requirement (DR), number of stations required to detect an earthquake
    DR = 4
    # Time to process (TTP) and send out an earthquake warning (s) (calculation, processing, and data latency)
    TTP = 4

    # default init takes a string, assumes that the string is the name of a shakemap xml grid file,
    # defaults to 'grid.xml'
    def __init__(self, xml='Data/grid.xml'):
        # parse an xml file using a name of a grid.xml
        self.tree = ET.parse(xml)
        self.root = self.tree.getroot()

        self.headers = []
        self.event = {}
        self.grid_spec = {}

        # Run through all the dictionaries/folders in the xml file and do things for each important one
        for t in self.root:
            # extract tag name from full tag info
            tag = t.tag.rpartition('}')[-1]

            # fill event dictionary with key value pairs for the event properties, make mag, depth, lat and lon floats
            if tag == 'event':
                for a in t.attrib:
                    if a in ['magnitude', 'depth', 'lat', 'lon']:
                        self.event[a] = float(t.attrib[a])
                    else:
                        self.event[a] = t.attrib[a]
                pass

            # fill grid_spec dictionary with key value pairs for the grid specs, make nlon & nlat ints, rest are floats
            if tag == 'grid_specification':
                for a in t.attrib:
                    if a in ['nlon', 'nlat']:
                        self.grid_spec[a] = int(t.attrib[a])
                    else:
                        self.grid_spec[a] = float(t.attrib[a])
                pass

            # get headers from the grid_fields
            if tag == 'grid_field':
                self.headers.append(t.attrib['name'])
                pass

            # create grid data array and variables from grid_data
            if tag == 'grid_data':
                # write grid_data.text to a file
                text_file = open('tmp/grid_data.txt', 'w')
                text_file.write(t.text.strip())
                text_file.close()
                # read the file with numpy and use headers as names for columns
                self.grid_array = np.genfromtxt('tmp/grid_data.txt', names=self.headers)
                # remove grid_data.txt, it is only needed for array creation
                os.remove('tmp/grid_data.txt')
                # create variables for columns of grid data
                self.lons = np.array([self.grid_array['LON']]).T
                self.lats = np.array([self.grid_array['LAT']]).T
                self.mmi = np.array([self.grid_array['MMI']]).T
                self.pga = np.array([self.grid_array['PGA']]).T
                self.pgv = np.array([self.grid_array['PGV']]).T

        # Calculate epicentral and hypocentral distances for each point
        self.distances_epi = np.array(
            [[getDistance(self.event['lat'], self.event['lon'], i, k)
              for (i, k) in zip(self.lats, self.lons)]]
        ).T
        self.distances_hypo = np.array(
            np.sqrt(np.square(self.distances_epi) + np.square(self.event['depth']))
        )
        # Calculate arrival times for p, s, and surface waves for each point
        self.arrivals_p = self.distances_hypo / Earthquake.vel_p
        self.arrivals_s = self.distances_hypo / Earthquake.vel_s
        self.arrivals_surf = self.distances_hypo / Earthquake.vel_surf
        self.detection_time = calculateDetectionTime(self.event['lon'], self.event['lat'], self.event['depth'], Earthquake.vel_p)

        # Calculate epicentral and hypocentral distances for each Active BB station
        # sta_dist = np.array(
        #     [getDistance(self.event['lat'], self.event['lon'], i, k)
        #      for (i, k) in zip(Earthquake.ActiveBBs['lat'], Earthquake.ActiveBBs['lon'])]
        # )
        # sta_dist = np.array(
        #     np.sqrt(np.square(sta_dist) + np.square(self.event['depth']))
        # )
        # Calculate P wave travel time to each station
        # self.station_arrivals_p = sta_dist / Earthquake.vel_p
        # self.detection_time = np.sort(self.station_arrivals_p)[Earthquake.DR - 1]
        # Calculate S wave and Surface wave Warning Time for each grid point
        self.warning_times_s = self.arrivals_s - (Earthquake.TTP + self.detection_time)
        self.warning_times_surf = self.arrivals_surf - (Earthquake.TTP + self.detection_time)

        # This next line makes negative warning times 0 (rename appropriately), left in for posterity's sake
        # self.warning_times = np.where(self.warning_times < 0, 0, self.warning_times)

        # Add one to total number of Earthquake classes created
        Earthquake.count += 1

        # Print out the finishing statement detailing the event
        print('Finished parsing grid.xml for: M{}, {}, at {} (ID:{})'.format(
            self.event['magnitude'], self.event['event_description'], self.event['event_timestamp'],
            self.event['event_id'])
        )
