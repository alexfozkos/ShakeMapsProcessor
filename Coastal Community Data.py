# Parses all of the Southern Coastline scenario grids and grabs data for points closest to select communities
# then dumps info into a json so I don't have to rerun 25 grids every time I want to try a new plotting format

import numpy as np
import pandas as pd
import UsefulFunctions as uf
import json
import os

# Dictionary of communities and their coords
community_dict = {'Sand Point': {'latlon': [55.3405, -160.4968]},
                  'Old Harbor': {'latlon': [57.2042, -153.3045]},
                  'Kodiak': {'latlon': [57.7900, -152.4072]},
                  'Homer': {'latlon': [59.6481, -151.5299]},
                  'Seward': {'latlon': [60.1048, -149.4421]},
                  'Anchorage': {'latlon': [61.2176, -149.8997]},
                  'Whittier': {'latlon': [60.7746, -148.6858]},
                  'Talkeetna': {'latlon': [62.3209, -150.1066]},
                  'Fairbanks': {'latlon': [64.8401, -147.7200]},
                  'Valdez': {'latlon': [61.1309, -146.3499]},
                  'Yakutat': {'latlon': [59.5453, -139.7268]},
                  'Haines': {'latlon': [59.2351, -135.4473]},
                  'Juneau': {'latlon': [58.3005, -134.4201]},
                  'Sitka': {'latlon': [57.0532, -135.3346]},
                  'Ketchikan': {'latlon': [55.3422, -131.6461]}}

# load in all the grids as earthquakes, save to another dictionary
eq_dict = {}
directory_in_str = 'Data/Southern Alaska Coast/grids'
directory = os.fsencode(directory_in_str)

for file in os.listdir(directory):
    filename = os.fsdecode(file)

    if filename.startswith("SouthernCoast"):
        eq_dict[filename] = uf.Earthquake(directory_in_str + '/' + filename)

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
    for label, eq in eq_dict.items():
        data[label] = {
            'wt_min': eq.warning_times_earlypeak[community['index']],
            'wt_max': eq.warning_times_latepeak[community['index']],
            'pga': eq.pga[community['index']],
            'pgv': eq.pgv[community['index']],
            'mmi': eq.mmi[community['index']],
            'h_dist': eq.distances_hypo[community['index']],
            'e_dist': eq.distances_epi[community['index']],
        }

with open('Data/Southern Alaska Coast/Community Data.json', 'w') as outfile:
    json.dump(community_dict, outfile)
