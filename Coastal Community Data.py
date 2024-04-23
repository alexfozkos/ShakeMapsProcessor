# Parses all of the Southern Coastline scenario grids and grabs data for points closest to select communities
# then dumps info into a json so I don't have to rerun 25 grids every time I want to try a new plotting format

import numpy as np
import pandas as pd
import UsefulFunctions as uf
import json
import os

# Dictionary of communities and their coords
community_dict = {'Sand Point': {'latlon': [55.3405, -160.4968]},
                  'Perryville': {'latlon': [55.9122, -159.1453]},
                  'Chignik': {'latlon': [56.2953, -158.4045]},
                  'Dillingham': {'latlon': [59.0395, -158.4633]},
                  'Akhiok': {'latlon': [56.9452, -154.1680]},
                  'Karluk': {'latlon': [57.5627, -154.4382]},
                  'Larsen Bay': {'latlon': [57.5368, -153.9819]},
                  'Old Harbor': {'latlon': [57.2042, -153.3045]},
                  'Chiniak': {'latlon': [57.6179, -152.2150]},
                  'Womens Bay': {'latlon': [57.7107, -152.5784]},
                  'Kodiak': {'latlon': [57.7900, -152.4072]},
                  'Port Lions': {'latlon': [57.8674, -152.8832]},
                  'Ouzinkie': {'latlon': [57.9233, -152.5019]},
                  'Nanwalek': {'latlon': [59.3568, -151.9217]},
                  'Port Graham': {'latlon': [59.3503, -151.8350]},
                  'Seldovia': {'latlon': [59.4385, -151.7150]},
                  'Homer': {'latlon': [59.6481, -151.5299]},
                  'Anchor Point': {'latlon': [59.7796, -151.8423]},
                  'Seward': {'latlon': [60.1048, -149.4421]},
                  'Chenega': {'latlon': [60.0649, -148.0112]},
                  'Hope': {'latlon': [60.9183, -149.6454]},
                  'Anchorage': {'latlon': [61.2176, -149.8997]},
                  'Girdwood': {'latlon': [60.9543, -149.1599]},
                  'Whittier': {'latlon': [60.7746, -148.6858]},
                  'Tatitlek': {'latlon': [60.8661, -146.6778]},
                  'Valdez': {'latlon': [61.1309, -146.3499]},
                  'Cordova': {'latlon': [60.5424, -145.7525]},
                  'Yakutat': {'latlon': [59.5453, -139.7268]},
                  'Skagway': {'latlon': [59.4572, -135.3145]},
                  'Haines': {'latlon': [59.2351, -135.4473]},
                  'Juneau': {'latlon': [58.3005, -134.4201]},
                  'Gustavus': {'latlon': [58.4126, -135.7389]},
                  'Hoonah': {'latlon': [58.1101, -135.4445]},
                  'Elfin Cove': {'latlon': [58.1939, -136.3450]},
                  'Pelican': {'latlon': [57.9604, -136.2300]},
                  'Sitka': {'latlon': [57.0532, -135.3346]},
                  'Port Alexander': {'latlon': [56.2467, -134.6476]},
                  'Port Protection': {'latlon': [56.3209, -133.6102]},
                  'Klawock': {'latlon': [55.5521, -133.0820]},
                  'Craig': {'latlon': [55.4769, -133.1358]},
                  'Hydaburg': {'latlon': [55.2074, -132.8275]},
                  'Kasaan': {'latlon': [55.5400, -132.4009]},
                  'Ketchikan': {'latlon': [55.3422, -131.6461]},
                  'Saxman': {'latlon': [55.3170, -131.5942]},
                  'Metlakatla': {'latlon': [55.1288, -131.5745]}}

# load in all the grids as earthquakes, save to another dictionary
eq_dict = {}
directory_in_str = 'Data/Southern Alaska Coast/grids'
directory = os.fsencode(directory_in_str)

for file in os.listdir(directory):
    filename = os.fsdecode(file)

    if filename.startswith("SouthernCoast"):
        # pull just the number out, this will make things easier to order later
        if len(filename) == 18:
            n = int((filename[13]))
        else:
            n = int(filename[13:15])
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

with open('Data/Southern Alaska Coast/Community Data.json', 'w') as outfile:
    json.dump(community_dict, outfile)
