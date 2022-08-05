# This file is for playing around with the xml parsing for the Earthquake Class, without messing things up for real
# Consider moving forward with dictionaries for each dictionary and attributes as keys, values as values
# instead of a bunch of 'loose' variables
# maybe also utilize pandas library for dataframes instead of making-unmaking a txt file for numpy?

import xml.etree.ElementTree as ET
import numpy as np
import os

# parse an xml file using a name of a grid.xml
tree = ET.parse('Data/misc/Iniskin_grid.xml')
root = tree.getroot()

headers = []
event = {}
grid_spec = {}

# Run through all the dictionaries/folders in the xml file and do things for each important one
for t in root:
    # extract tag name from full tag info
    tag = t.tag.rpartition('}')[-1]

    # fill a dictionary called event with key value pairs for the event properties, make mag, depth, lat and lon floats
    if tag == 'event':
        for a in t.attrib:
            if a in ['magnitude', 'depth', 'lat', 'lon']:
                event[a] = float(t.attrib[a])
            else:
                event[a] = t.attrib[a]

    # fill grid_spec dictionary with key value pairs for the grid specs, make nlon & nlat ints, rest should be floats
    if tag == 'grid_specification':
        for a in t.attrib:
            if a in ['nlon', 'nlat']:
                grid_spec[a] = int(t.attrib[a])
            else:
                grid_spec[a] = float(t.attrib[a])

    # get headers from the grid_fields
    if tag == 'grid_field':
        headers.append(t.attrib['name'])

    # create grid data array and variables from grid_data
    if tag == 'grid_data':
        # write grid_data.text to a file
        text_file = open('tmp/grid_data.txt', 'w')
        text_file.write(t.text.strip())
        text_file.close()
        # read the file with numpy and use headers as names for columns
        grid_array = np.genfromtxt('tmp/grid_data.txt', names=headers)
        # remove grid_data.txt, it is only needed for array creation
        # os.remove('tmp/grid_data.txt')
        # create variables for columns of grid data
        lons = np.array([grid_array['LON']]).T
        lats = np.array([grid_array['LAT']]).T
        mmi = np.array([grid_array['LAT']]).T
        pga = np.array([grid_array['LAT']]).T
        pgv = np.array([grid_array['LAT']]).T

