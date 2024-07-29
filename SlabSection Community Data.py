# Parses all of the Southern Coastline scenario grids and grabs data for points closest to select communities
# then dumps info into a json so I don't have to rerun 25 grids every time I want to try a new plotting format

import numpy as np
import pandas as pd
import UsefulFunctions as uf
import json
import os

# Dictionary of communities and their coords

# Dictionary of communities and their coords
community_dict = {'Homer': {'latlon': [59.6481, -151.5299]},
                  'Anchor Point': {'latlon': [59.7796, -151.8423]},
                  'Soldotna': {'latlon': [60.4864, -151.0572]},
                  'Seward': {'latlon': [60.1048, -149.4421]},
                  'Chenega': {'latlon': [60.0649, -148.0112]},
                  'Hope': {'latlon': [60.9183, -149.6454]},
                  'Anchorage': {'latlon': [61.2176, -149.8997]},
                  'Girdwood': {'latlon': [60.9543, -149.1599]},
                  'Wasilla': {'latlon': [61.5809, -149.4411]},
                  'Palmer': {'latlon': [61.5994, -149.1146]},
                  'Whittier': {'latlon': [60.7746, -148.6858]},
                  'Tatitlek': {'latlon': [60.8661, -146.6778]},
                  'Valdez': {'latlon': [61.1309, -146.3499]},
                  'Cordova': {'latlon': [60.5424, -145.7525]},
                  'Talkeetna': {'latlon': [62.3209, -150.1066]}}

# load in all the grids as earthquakes, save to another dictionary
eq_dict = {}
directory_in_str = 'Data/Down Dip/grids'
directory = os.fsencode(directory_in_str)

for i in range(1, 14):
    eq_dict[i] = uf.Earthquake(directory_in_str + f'/SlabSection{i}.xml')


# grabs the coordniate list from the grid, should all be the same grid for each eq
# grab one of the keys, not sure how to do this elegantly

grid_lats = eq_dict[1].lats
grid_lons = eq_dict[1].lons

# get the closest point in the shakemap grid to each community
for name in community_dict.keys():
    lat = community_dict[name]['latlon'][0]
    lon = community_dict[name]['latlon'][1]
    subtracted_list = np.hstack((grid_lats - lat, grid_lons - lon))
    nearest_index = np.nanargmin(np.sum(subtracted_list ** 2, axis=1))
    community_dict[name]['index'] = int(nearest_index)
    print(community_dict[name]['index'])

for community, data in community_dict.items():
    data['scenarios'] = {}
    for label, eq in eq_dict.items():
        data['scenarios'][label] = {
            'wt_min': eq.warning_times_earlypeak[data['index'], 0],
            'wt_max': eq.warning_times_latepeak[data['index'], 0],
            'pga': eq.pga[data['index'], 0],
            'pgv': eq.pgv[data['index'], 0],
            'mmi': eq.mmi[data['index'], 0],
            'h_dist': eq.distances_hypo[data['index'], 0],
            'e_dist': eq.distances_epi[data['index'], 0],
        }

with open('Data/Down Dip/Community Data.json', 'w') as outfile:
    json.dump(community_dict, outfile)
