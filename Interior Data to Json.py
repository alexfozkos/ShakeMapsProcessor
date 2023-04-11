# Parses all of the Southern Coastline scenario grids and grabs data for points closest to select communities
# then dumps info into a json so I don't have to rerun 25 grids every time I want to try a new plotting format

import numpy as np
import UsefulFunctions as uf
import json

community_dict = {'Anchorage': {'latlon': [61.2167, -149.8936]},
                  'Fairbanks': {'latlon': [64.8401, -147.7200]},
                  'North Pole': {'latlon': [64.7552, -147.3534]},
                  'Healy': {'latlon': [63.8697, -149.0215]},
                  'Cantwell': {'latlon': [63.3905, -148.9018]},
                  'Glennallen': {'latlon': [62.1081, -145.5340]},
                  'Fort Greely': {'latlon': [63.9800, -145.7424]},
                  'Eielson Air Force Base': {'latlon': [64.6638, -147.0992]},
                  'Fort Wainwright': {'latlon': [64.8278, -147.6429]},
                  'Clear Space Force Station': {'latlon': [64.2912, -149.1595]},
                  'Whittier': {'latlon': [60.7667, -148.7000]},
                  'Talkeetna': {'latlon': [62.3333, -150.1000]}
                  }

eq_dict = {'tin': uf.Earthquake('Data/Interior Crustal/grids/Tintina.xml'),
           'rsz': uf.Earthquake('Data/Interior Crustal/grids/Rampart.xml'),
           'msz': uf.Earthquake('Data/Interior Crustal/grids/Minto_Flats.xml'),
           'fsz': uf.Earthquake('Data/Interior Crustal/grids/Fairbanks.xml'),
           'ssz': uf.Earthquake('Data/Interior Crustal/grids/Salcha.xml'),
           'nf': uf.Earthquake('Data/Interior Crustal/grids/Northern_Foothills.xml'),
           'den1': uf.Earthquake('Data/Interior Crustal/grids/Denali_1.xml'),
           'den2': uf.Earthquake('Data/Interior Crustal/grids/Denali_2.xml'),
           'den3': uf.Earthquake('Data/Interior Crustal/grids/Denali_3.xml'),
           'den4': uf.Earthquake('Data/Interior Crustal/grids/Denali_4.xml'),
           'den5': uf.Earthquake('Data/Interior Crustal/grids/Denali_5.xml'),
           'cm2': uf.Earthquake('Data/Interior Crustal/grids/Castle_1.xml'),
           'cm1': uf.Earthquake('Data/Interior Crustal/grids/Castle_2.xml')}

# eqlist = [alu0, alu2, alu4, alu6, alu8, alu10, alu12]
# eqlabels = ['ALU0', 'ALU2', 'ALU4', 'ALU6', 'ALU8', 'ALU10', 'ALU12']
latlonlist = np.hstack((eq_dict['tin'].lats, eq_dict['tin'].lons))

for key in community_dict.keys():
    # community_dict[key]['index'] = int(np.all(latlonlist == community_dict[key]['closest_latlon'], axis=1).nonzero()[0][0])
    lat = community_dict[key]['latlon'][0]
    lon = community_dict[key]['latlon'][1]
    subtracted_list = np.hstack((eq_dict['tin'].lats - lat, eq_dict['tin'].lons - lon))
    nearest_index = np.nanargmin(np.sum(subtracted_list**2, axis=1))
    community_dict[key]['index'] = int(nearest_index)
    print(community_dict[key]['index'])
# print(ancindex)
for label, eq in eq_dict.items():
    for city in community_dict.values():
        if 'wtfast' not in city:
            city['wtfast'] = []
        city['wtfast'].append(float(np.around(eq.warning_times_s[city['index'], 0], decimals=1)))
        if 'wtslow' not in city:
            city['wtslow'] = []
        city['wtslow'].append(float(np.around(eq.warning_times_slow[city['index'], 0], decimals=1)))
        if 'pga' not in city:
            city['pga'] = []
        city['pga'].append(eq.pga[city['index'], 0])
        if 'pgv' not in city:
            city['pgv'] = []
        city['pgv'].append(eq.pgv[city['index'], 0])
        if 'mmi' not in city:
            city['mmi'] = []
        city['mmi'].append(eq.mmi[city['index'], 0])

with open('Data/Interior Crustal/Interior Community Data.json', 'w') as outfile:
    json.dump(community_dict, outfile)
