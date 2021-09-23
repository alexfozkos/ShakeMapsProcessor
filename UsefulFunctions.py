import xml.etree.ElementTree as ET
import math
import numpy as np


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

