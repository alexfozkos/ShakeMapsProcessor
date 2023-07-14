import xml.etree.ElementTree as ET
import math
import numpy as np
from numpy import sin, cos, pi
import requests
import os
import pandas as pd

PROJ_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(PROJ_ROOT, 'Data')

# old activebbs.txt
# ActiveBBs = np.genfromtxt('Data/activeBBs.txt',
#                           delimiter=[8, 9, 12, 8, 50],
#                           # encoding='utf-8',
#                           dtype=[('sta', 'U5'), ('lat', 'f8'), ('lon', 'f8'), ('elev', 'f8'), ('staname', 'U50')],
#                           # usecols=(0, 1, 2, 3),
#                           autostrip=True,
#                           )

# uses csv file stations_kept.csv
ActiveBBs = pd.read_csv(f'{DATA_PATH}/stations_Kept.csv', quotechar='"')
mechs_df = pd.read_csv(f'{DATA_PATH}/mechs.txt')

# downloads grid.xml from shakemaps url because I can't figure out how to download it otherwise
def download(url):
    response = requests.get(url)
    with open(f'{DATA_PATH}/misc/grid.xml', 'wb') as file:
        file.write(response.content)


def update_mechstxt(name, mech):
    # add name and mechanism to the mechs.txt file (if not already) for rupture duration calculation in uf
    # create line for the given scenario name an mech
    mech_string = name + ',' + mech + '\n'
    # checks for the mech_string in mechs.txt
    with open("Data/mechs.txt", "r+") as file:
        for line in file:
            if mech_string == line:
                break
        else:  # not found, we are at the eof
            file.write(mech_string)  # append missing data


def km2lat(d):
    return d / 110.574


def km2lon(d, lat):
    return d / (111.320 * cos(np.deg2rad(lat)))


# get closest 1d index to a given lat lon in the column of grid lats and lons
def getNearestIndex(grid_lons, grid_lats, search_lon, search_lat):
    subtracted_list = np.hstack((grid_lons - search_lon, grid_lats - search_lat))
    nearest_index = np.nanargmin(np.sum(subtracted_list**2, axis=1))
    return nearest_index


def createPlane(lon0, lat0, Mw, D, strike, dip, mech):
    #       dipping northwest (towards 8)
    #                    1
    #
    #                           2
    #
    #           8                       3
    #
    #                 '0'
    #
    #   7                      4
    #
    #          6
    #
    #                 5

    theta = np.deg2rad(dip)  # convert dip to radians
    angle = np.deg2rad(360 - strike + 90)  # Convert strike to positive angle from x axis, and to radians

    if mech == 'int':  # Table 2 (Allen & Hayes 2017), interface rupture
        L = 10 ** (-2.90 + 0.63 * Mw)  # km, length of fault
        WL = 10 ** (0.39 + 0.74 * np.log10(L))  # km, width of fault
        W1 = 10 ** (-0.86 + 0.35 * Mw)
        W = 10 ** (-1.91 + 0.48 * Mw)  # W2
        Wproj = W * cos(theta)  # find the projected width of the fault
        deld = 0.5 * W * sin(theta)  # find the change in depth from the center to the top/bottom of the fault

    elif mech == 'r':  # Table 1 (Thingbaijam et al. 2017), reverse fault
        L = 10 ** (-2.693 + 0.614 * Mw)
        W = 10 ** (-1.669 + 0.435 * Mw)
        Wproj = W * cos(theta)
        deld = 0.5 * W * sin(theta)

    elif mech == 'ss':  # Table 5 (Allen & Hayes 2017), offshore strike slip rupture
        L = 10 ** (-2.81 + 0.63 * Mw)
        W_L = 10 ** (-0.22 + 0.74 * np.log10(L))
        W = 10 ** (-1.39 + 0.35 * Mw)
        Wproj = W * cos(theta)
        deld = 0.5 * W * sin(theta)

    elif mech == 'is':  # Table 5 (Allen & Hayes 2017), inslab rupture
        L = 10 ** (-3.03 + 0.63 * Mw)
        W = 10 ** (-1.01 + 0.35 * Mw)
        Wproj = W * cos(theta)
        deld = 0.5 * W * sin(theta)

    elif mech == 'or':  # Table 5 (Allen & Hayes 2017), outer-rise rupture
        L = 10 ** (-2.87 + 0.63 * Mw)
        W = 10 ** (-1.18 + 0.35 * Mw)
        Wproj = W * cos(theta)
        deld = 0.5 * W * sin(theta)

    else:
        L = 1
        W = 1
        Wproj = W * cos(theta)
        deld = 0.5 * W * sin(theta)

    print('''Fault Plane Parameters
    Strike: {}
    Dip: {}
    Length: {}
    Width: {}
    Projected Width: {}
    Lower depth: {}
    Upper depth: {}
    '''.format(strike, dip, L, W, Wproj, D + deld, D - deld))
    # calculate points of the plane, midpoints first
    x2 = 0.5 * L * cos(angle - pi)
    # print(type(lon0))
    # print(lon0)
    # print(type(km2lon(x2, lat0)))
    lon2 = lon0 + km2lon(x2, lat0)
    y2 = 0.5 * L * sin(angle - pi)
    lat2 = lat0 + km2lat(y2)
    d2 = D
    p2 = (lon2-360, lat2, d2)

    x6 = 0.5 * L * cos(angle)
    lon6 = lon0 + km2lon(x6, lat0)
    y6 = 0.5 * L * sin(angle)
    lat6 = lat0 + km2lat(y6)
    d6 = D
    p6 = (lon6-360, lat6, d6)

    x8 = 0.5 * Wproj * cos(angle - pi / 2)
    lon8 = lon0 + km2lon(x8, lat0)
    y8 = 0.5 * Wproj * sin(angle - pi / 2)
    lat8 = lat0 + km2lat(y8)
    d8 = D + deld
    p8 = (lon8-360, lat8, d8)

    x4 = 0.5 * Wproj * cos(angle + pi / 2)
    lon4 = lon0 + km2lon(x4, lat0)
    y4 = 0.5 * Wproj * sin(angle + pi / 2)
    lat4 = lat0 + km2lat(y4)
    d4 = D - deld
    p4 = (lon4-360, lat4, d4)

    # Corners, use midpoints as reference
    x1 = 0.5 * L * cos(angle - pi)
    lon1 = lon8 + km2lon(x1, lat0)
    y1 = 0.5 * L * sin(angle - pi)
    lat1 = lat8 + km2lat(y1)
    d1 = D + deld
    p1 = (lon1-360, lat1, d1)

    x7 = 0.5 * L * cos(angle)
    lon7 = lon8 + km2lon(x7, lat0)
    y7 = 0.5 * L * sin(angle)
    lat7 = lat8 + km2lat(y7)
    d7 = D + deld
    p7 = (lon7-360, lat7, d7)

    x3 = 0.5 * L * cos(angle - pi)
    lon3 = lon4 + km2lon(x3, lat0)
    y3 = 0.5 * L * sin(angle - pi)
    lat3 = lat4 + km2lat(y3)
    d3 = D - deld
    p3 = (lon3-360, lat3, d3)

    x5 = 0.5 * L * cos(angle)
    lon5 = lon4 + km2lon(x5, lat0)
    y5 = 0.5 * L * sin(angle)
    lat5 = lat4 + km2lat(y5)
    d5 = D - deld
    p5 = (lon5-360, lat5, d5)

    p0 = (lon0, lat0, D)
    x = [x1, x2, x3, x4, x5, x6, x7, x8]
    y = [y1, y2, y3, y4, y5, y6, y7, y8]
    points = [p0, p1, p2, p3, p4, p5, p6, p7, p8]
    # for point in points:
    #     print(point)
    # print(x)
    # print(y)
    return points, [L, W]


def getLength(Mw, mech):
    # This calculates the fault length of an earthquake given magnitude and rupture mechanism
    if mech == 'int':  # Table 2, interface rupture
        L = 10 ** (-2.90 + 0.63 * Mw)  # km, length of fault
    elif mech == 'r':  # Table 2 in drive reverse fault (where did these numbers come from? Investigate)
        L = 10 ** (-2.693 + 0.614 * Mw)  # km, length of fault
    elif mech == 'ss':  # Table 5, strike slip rupture
        L = 10 ** (-2.81 + 0.63 * Mw)  # km, length of fault
    elif mech == 'is':  # Table 5 in drive inslab
        L = 10 ** (-3.03 + 0.63 * Mw)  # km, length of fault
    elif mech == 'or':  # Table 5 outer rise
        L = 10 ** (-2.87 + 0.63 * Mw)  # km, length of fault
    else:
        L = 1

    return L


def getMech(name):  # tries to get the mech given a scneario name
    if (mechs_df['name'] == name).sum() > 0:  # if the name is in the mechs list
        return mechs_df.loc[mechs_df['name'] == name]['mech'].iloc[0]  # return the mech
    else:
        return None  # otherwise return none


def getDuration(name, Mw, rup_vel=6.7*.6*.7, rup_dir='bi'):  # tries to calculate rupture duration for a scenario
    mech = getMech(name)
    if mech == None:
        return 0
    length = getLength(Mw, mech)
    if rup_dir == 'bi':
        return length/2/rup_vel
    elif rup_dir == 'uni':
        return length/rup_vel
    else:
        return 0


# create medians and means of y values for each step in x
# defaults to mmi step of 0.1
def meansAndMedians(x, y, step=0.1):
    y_means = []
    y_medians = []
    x_vals = np.arange(x.min(), x.max()+step, step)
    for k in x_vals:
        mask = np.isclose(x, k)
        y_means.append(np.mean(y[mask]))
        y_medians.append(np.median(y[mask]))

    return [y_means, y_medians]

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
            midway = (x_space[i] + x_space[i + 1]) / 1.985
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
         for (i, k) in zip(ActiveBBs['lat'], ActiveBBs['lon'])]
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
    sta_list = np.vstack((ActiveBBs['lon'], ActiveBBs['lat'], sta_dist_e, sta_arr_p))
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
    adotb = sum(a[i] * b[i] for i in range(len(a)))
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
    # ActiveBBs = np.genfromtxt('Data/activeBBs.txt',
    #                           delimiter=[8, 9, 12, 8, 50],
    #                           # encoding='utf-8',
    #                           dtype=[('sta', 'U5'), ('lat', 'f8'), ('lon', 'f8'), ('elev', 'f8'), ('staname', 'U50')],
    #                           # usecols=(0, 1, 2, 3),
    #                           autostrip=True,
    #                           )
    count = 0

    # wave velocities (km/s)
    vel_p = 6.7
    vel_s = vel_p * 0.6
    vel_slow = 2.5  # based on looking at apparent velociies of recent significant Alaska earthquakes

    # Tolerances for early and late peak moment rate
    # normalized centroid time interquartile limits
    q25 = 0.38
    q75 = 0.64

    # rupture velocity calculation
    vel_rup = vel_s * 0.7

    # Detection Requirement (DR), number of stations required to detect an earthquake
    DR = 4
    # Time to process (TTP) and send out an earthquake warning (s) (calculation, processing, and data latency)
    TTP = 4

    # default init takes a string, assumes that the string is the name of a shakemap xml grid file,
    # defaults to 'grid.xml'
    def __init__(self, xml=f'{DATA_PATH}/grid.xml'):
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

        # get rupture duration estimate
        if self.event['event_id'][-2:] in ['NW', 'NE', 'SW', 'SE', 'NN', 'WW', 'EE', 'SS']:
            self.rupture_type = 'uni'
        else:
            self.rupture_type = 'bi'

        self.duration = getDuration(self.event['event_id'], self.event['magnitude'], self.vel_rup, self.rupture_type)
        self.half_dur = self.duration/2

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
        self.arrivals_slow = self.distances_hypo / Earthquake.vel_slow
        self.detection_time = calculateDetectionTime(self.event['lon'], self.event['lat'], self.event['depth'],
                                                     Earthquake.vel_p)
        self.station_distances = np.array(
            [getDistance(self.event['lat'], self.event['lon'], i, k)
             for (i, k) in zip(ActiveBBs['lat'], ActiveBBs['lon'])]
        )
        # Calculate epicentral and hypocentral distances for each Active BB station
        # sta_dist = np.array(
        #     [getDistance(self.event['lat'], self.event['lon'], i, k)
        #      for (i, k) in zip(ActiveBBs['lat'], ActiveBBs['lon'])]
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
        self.warning_times_slow = self.arrivals_slow - self.alert_time
        # add half duration
        # self.warning_times_s_dur = self.warning_times_s + self.half_dur
        # self.warning_times_slow_dur = self.warning_times_slow + self.half_dur
        # add early and late arrivals of peak source time function
        self.early_peak_time = self.duration * Earthquake.q25
        self.late_peak_time = self.duration * Earthquake.q75
        self.warning_times_earlypeak = self.warning_times_s + self.early_peak_time
        self.warning_times_latepeak = self.warning_times_s + self.late_peak_time


        # This next line makes negative warning times 0 (rename appropriately), left in for posterity's sake
        # self.warning_times = np.where(self.warning_times < 0, 0, self.warning_times)

        # Add one to total number of Earthquake classes created
        Earthquake.count += 1

        # Print out the finishing statement detailing the event
        print('Finished parsing grid.xml for: M{}, {}, at {} (ID:{})'.format(
            self.event['magnitude'], self.event['event_description'], self.event['event_timestamp'],
            self.event['event_id'])
        )
