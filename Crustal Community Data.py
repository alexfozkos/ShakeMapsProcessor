# Parses all of the Southern Coastline scenario grids and grabs data for points closest to select communities
# then dumps info into a json so I don't have to rerun 25 grids every time I want to try a new plotting format

import numpy as np
import pandas as pd
import UsefulFunctions as uf
import json
import os

# Dictionary of communities and their coords
community_dict = {'Fairbanks': {'latlon': [64.8401, -147.7200]},
                  'Fort Wainwright': {'latlon': [64.8278, -147.6429]},
                  'North Pole': {'latlon': [64.7552, -147.3534]},
                  'Eielson Air Force Base': {'latlon': [64.6638, -147.0992]},
                  'Salcha': {'latlon': [64.5605, -147.0356]},
                  'Clear Space Force Station': {'latlon': [64.2912, -149.1595]},
                  'Delta Junction': {'latlon': [64.0401, -145.7344]},
                  'Fort Greely': {'latlon': [63.9800, -145.7424]},
                  'Healy': {'latlon': [63.8697, -149.0215]},
                  'Cantwell': {'latlon': [63.3905, -148.9018]},
                  'Talkeetna': {'latlon': [62.3209, -150.1066]},
                  'Glennallen': {'latlon': [62.1081, -145.5340]},
                  'Wasilla': {'latlon': [61.5809, -149.4411]},
                  'Palmer': {'latlon': [61.5994, -149.1146]},
                  'Anchorage': {'latlon': [61.2167, -149.8936]},
                  'Whittier': {'latlon': [60.7746, -148.6858]},
                  }

# load in all the grids as earthquakes, save to another dictionary
eq_dict = {}
directory_in_str = 'Data/Interior Crustal/grids'
directory = os.fsencode(directory_in_str)

for file in os.listdir(directory):
    filename = os.fsdecode(file)

    if filename.startswith("Crustal"):
        # pull just the number out, this will make things easier to order later
        if len(filename) == 12:
            n = int((filename[7]))
        else:
            n = int(filename[7:9])
        eq_dict[n] = uf.Earthquake(directory_in_str + '/' + filename)

    else:
        continue

# grabs the coordniate list from the grid, should all be the same grid for each eq
# grab one of the keys, not sure how to do this elegantly
placeholder_name = list(eq_dict.keys())[0]
grid_lats = eq_dict[placeholder_name].lats
grid_lons = eq_dict[placeholder_name].lons

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

with open('Data/Interior Crustal/Community Data.json', 'w') as outfile:
    json.dump(community_dict, outfile)
