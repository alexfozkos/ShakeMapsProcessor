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

# creates a set of points to draw a polygon around a set of x y data, done by slicing the
# x points into chunks and finding the min and max y values in that slice.
def createPolygon(colx, coly, n=250, invert=True, xscale='log', step=0.1):
    data = np.hstack((colx, coly))  # stack together
    data = data[data[:, 0].argsort()]  # sort by x
    if invert:  # invert data if true, useful for PGA
        data = data[::-1]
    x_sorted = data[:, 0]
    y_sorted = data[:, 1]
    if xscale == 'lin':
        x_space = np.arange(start=x_sorted.min(), stop=(x_sorted.max() + step), step=step)
    elif xscale == 'log':
        x_space = np.logspace(-4, 2, num=n)
    # if invert:
    x_space = x_space[::-1]
    # print(x_space[-1::-10])
    maxmins = np.zeros((2, 1))
    x_mids = np.array([])
    for i in range(x_space.shape[0] - 1):
        slice_index = np.where((x_sorted < x_space[i]) & (x_sorted >= x_space[i + 1]), [True], [False])
        y_slice = y_sorted[slice_index]
        if np.size(y_slice) == 0:
            continue
        topbot = np.array([[np.max(y_slice)], [np.min(y_slice)]])
        maxmins = np.hstack((maxmins, topbot))
        if xscale == 'lin':
            midway = (x_space[i] + x_space[i + 1]) / 2
        elif xscale == 'log':
            midway = np.exp((np.log(x_space[i]) + np.log(x_space[i + 1])) / 2)
        x_mids = np.append(x_mids, midway)
    maxmins = maxmins[:, 1:]  # pop off that inital 0 column
    y_maxes = maxmins[0, :]
    y_mins = maxmins[1, :]
    # reverse mins so we can draw from left to right, up thorugh the maxes and back  down left through the mins
    y_mins = y_mins[::-1]
    y_points = np.append(y_maxes, y_mins)
    x_mids = np.append(x_mids, x_mids[::-1])  # add the same mid points but backwards for the mins
    x_mids = np.append(x_mids, x_mids[0])  # pad these two at the end to create a closed polygon
    y_points = np.append(y_points, y_points[0])
    return x_mids, y_points


def calculateDetectionTime(lon, lat, depth, vp):
    # Set our station criteria
    gap_criteria = 300  # azimuthal gap
    dist_criteria = 0  # min distance
    angle_criteria = 30  # minimum angle between station vectors (think cone projection, 3D gap)
    station_angle_criteria = 60  # vertical angle needed for 12
    # get epicentral distances for each bb station from eq, we care for station criteria
    sta_dist_e = np.array(
        [getDistance(lat, lon, i, k)
         for (i, k) in zip(Earthquake.ActiveBBs['lat'], Earthquake.ActiveBBs['lon'])]
    )
    # get hypocentral distances, we care for arrival times
    sta_dist_h = np.array(
        np.sqrt(np.power(sta_dist_e, 2) + depth ** 2)
    )
    # sta_dist_col = sta_dist.reshape(sta_dist.shape[0], 1)

    # Calculate P wave travel time to each station
    sta_arr_p = sta_dist_h / vp
    # sta_arr_p_col = sta_arr_p.reshape(sta_arr_p.shape[0], 1)

    # create array of columns of stations lons, lats, epicentral distances, and p arrival times
    sta_list = np.vstack((Earthquake.ActiveBBs['lon'], Earthquake.ActiveBBs['lat'], sta_dist_e, sta_arr_p))
    # turn into rows of data instead of columns (lon, lat, dist, p arrival)
    sta_list = sta_list.transpose()
    # sort the rows (each stations data) by the arrival times
    sta_list = sta_list[sta_list[:, 3].argsort()]

    n = 0  # Increasing number of stations
    # initialize criteria variables
    max_gap = 360  # Azimuthal Gap tacker
    max_dist = 0  # distance tracker
    min_dist = np.min(sta_list[0, 2])
    max_angle = 0
    detection_time = -1
    # time to check for criteria,
    # if we go out of bounds on our list of stations,
    # then we don't meet our criteria to detect the earthquake :(
    try:
        while max_gap >= gap_criteria or max_angle <= angle_criteria:
            # The x closest stations, increase by one each time we fail to meet criteria
            current_stations = sta_list[:Earthquake.DR + n, :]
            # get our would be detection time (latest p arrival) if we pass this loop
            detection_time = np.max(current_stations[-1, 3])
            # get epicentral distance of furthest station we are looking at
            max_dist = np.max(current_stations[-1, 2])
            # find bearings to each station
            bearings = np.array([])  # bearings
            for i in range(0, Earthquake.DR + n):
                bearings = np.append(bearings, getBearing(lon, lat, current_stations[i, 0], current_stations[i, 1]))
            # print(bearings)
            # sort the bearings in clockwise order
            bearings = np.sort(bearings)
            # find gaps between each bearing and the bearing before it
            gaps = np.array([])  # gaps
            for i in range(1, Earthquake.DR + n):
                gaps = np.append(gaps, bearings[i] - bearings[i - 1])
            gaps = np.append(gaps, 360 - np.sum(gaps))  # add last missing gap between first and last
            # get largest azimuthal gap
            max_gap = np.max(gaps)

            # vector angle criteria
            # create xyz vectors for each point, relative to epicenter
            station_vectors = {}
            for i in range(Earthquake.DR + n):
                theta = getTheta(lon, lat, current_stations[i, 0], current_stations[i, 1])
                # print(np.degrees(theta))
                x, y = getXY(current_stations[i, 2], theta)
                z = depth
                vector = [x, y, z]
                station_vectors[i] = vector
            vector_angles = np.zeros((Earthquake.DR + n, Earthquake.DR + n))
            for i in range(Earthquake.DR + n):
                for j in range(Earthquake.DR + n):
                    if i == j:
                        vector_angles[i, j] = 0
                    else:
                        vector_angles[i, j] = getAngle(station_vectors[i], station_vectors[j])
            # print(station_vectors)
            # print(vector_angles)
            max_angle = np.max(vector_angles)

            n += 1  # increase our station count in case we have to check again
    except:
        print('Failed to meet criteria for this event')
        detection_time = -1
    # print(vector_angles)
    print('''   ~~Detection stats~~
    Used a maximum azimuthal gap of {} degrees and minimum station vector angle of {} km
    Number of stations needed: {}
    Detection Time: {}
    Azimuthal Gap: {}
    Max Vector Angle: {}
    Maximum Epicentral Distance: {}'''.format(gap_criteria, angle_criteria, Earthquake.DR + n - 1, detection_time,
                                              max_gap, max_angle, max_dist))

    return detection_time


# function for finding the bearing between two lat lon points
# https://towardsdatascience.com/calculating-the-bearing-between-two-geospatial-coordinates-66203f57e4b4
def getBearing(lon1, lat1, lon2, lat2):
    a = {'lat': np.radians(lat1), 'lon': np.radians(lon1)}  # epicenter
    b = {'lat': np.radians(lat2), 'lon': np.radians(lon2)}  # station
    dL = b['lon'] - a['lon']
    X = np.cos(b['lat']) * np.sin(dL)
    Y = np.cos(a['lat']) * np.sin(b['lat']) - np.sin(a['lat']) * np.cos(b['lat']) * np.cos(dL)
    bearing = np.arctan2(X, Y)
    bearing = (np.degrees(bearing) + 360) % 360
    return bearing


# function for finding the angle from the positive x axis (due east) between two lat lon points
def getTheta(lon1, lat1, lon2, lat2):
    a = {'lat': np.radians(lat1), 'lon': np.radians(lon1)}  # epicenter
    b = {'lat': np.radians(lat2), 'lon': np.radians(lon2)}  # station
    dL = b['lon'] - a['lon']
    X = np.cos(b['lat']) * np.sin(dL)
    Y = np.cos(a['lat']) * np.sin(b['lat']) - np.sin(a['lat']) * np.cos(b['lat']) * np.cos(dL)
    theta = np.arctan2(Y, X)
    # theta = theta - np.pi/2  # shift to positive x axis
    # return angle in RADIANS, not degrees, so we can keep using for trig calculations
    return theta


# take a length and angle and find X Y components, top down view of epicenter as 0,0 and epicentral distance to point
# theta should be in radians
def getXY(d, theta):
    x = d * np.cos(theta)
    y = d * np.sin(theta)
    return x, y


# get angle between two vectors
def getAngle(a, b):
    # adotb = np.vdot(a, b)
    adotb = sum(a[i]*b[i] for i in range(len(a)) )
    amag = np.sqrt(np.vdot(a, a))
    bmag = np.sqrt(np.vdot(b, b))
    # print(adotb, amag, bmag)
    angle = np.arccos(adotb / (amag * bmag))
    # final product for angle calculation, so we return it in degrees to check against criteria
    return np.degrees(angle)


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
        print('Start of Parsing for {}'.format(xml))

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
                # make the temporary directory if it doesn't exists
                if not os.path.exists('tmp'):
                    os.makedirs('tmp')
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
        self.detection_time = calculateDetectionTime(self.event['lon'], self.event['lat'], self.event['depth'],
                                                     Earthquake.vel_p)
        self.station_distances = np.array(
            [getDistance(self.event['lat'], self.event['lon'], i, k)
             for (i, k) in zip(Earthquake.ActiveBBs['lat'], Earthquake.ActiveBBs['lon'])]
        )
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
        self.alert_time = Earthquake.TTP + self.detection_time
        self.warning_times_s = self.arrivals_s - self.alert_time
        self.warning_times_surf = self.arrivals_surf - self.alert_time

        # This next line makes negative warning times 0 (rename appropriately), left in for posterity's sake
        # self.warning_times = np.where(self.warning_times < 0, 0, self.warning_times)

        # Add one to total number of Earthquake classes created
        Earthquake.count += 1

        # Print out the finishing statement detailing the event
        print('Finished parsing grid.xml for: M{}, {}, at {} (ID:{})'.format(
            self.event['magnitude'], self.event['event_description'], self.event['event_timestamp'],
            self.event['event_id'])
        )
