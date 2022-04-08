import numpy as np
import UsefulFunctions as uf
import json

community_dict = {'Sand Point': {'latlon': [55.3333, -160.5000]}, 'Old Harbor': {'latlon': [57.2000, -153.3000]},
              'Kodiak': {'latlon': [57.9000, -152.4000]}, 'Homer': {'latlon': [59.6333, -151.5333]},
              'Seward': {'latlon': [60.1000, -149.4333]}, 'Anchorage': {'latlon': [61.2000, -149.9000]},
              'Whittier': {'latlon': [60.7667, -148.7000]}, 'Talkeetna': {'latlon': [62.3333, -150.1000]},
              'Fairbanks': {'latlon': [64.8333, -147.7333]}, 'Valdez': {'latlon': [61.1333, -146.3333]},
              'Yakutat': {'latlon': [59.5333, -139.7333]}, 'Haines': {'latlon': [59.2333, -135.4333]},
              'Juneau': {'latlon': [58.3000, -134.4333]}, 'Sitka': {'latlon': [57.0667, -135.3333]},
              'Ketchikan': {'latlon': [55.3333, -131.6333]}}
# coord_dict[''] = {'latlon': []}

eq_dict = {'alu1': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU1grid.xml'),
           'alu2': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU2grid.xml'),
           'alu3': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU3grid.xml'),
           'alu4': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU4grid.xml'),
           'alu5': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU5grid.xml'),
           'alu6': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU6grid.xml'),
           'alu7': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU7grid.xml'),
           'alu8': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU8grid.xml'),
           'alu9': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU9grid.xml'),
           'alu10': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU10grid.xml'),
           'alu11': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU11grid.xml'),
           'alu12': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU12grid.xml'),
           'alu13': uf.Earthquake('Data/Southern Alaska Coast/grids/ALU13grid.xml'),
           'cse1': uf.Earthquake('Data/Southern Alaska Coast/grids/CSE1grid.xml'),
           'cse2': uf.Earthquake('Data/Southern Alaska Coast/grids/CSE2grid.xml'),
           'qcf1': uf.Earthquake('Data/Southern Alaska Coast/grids/QCF1grid.xml'),
           'qcf2': uf.Earthquake('Data/Southern Alaska Coast/grids/QCF2grid.xml'),
           'qcf3': uf.Earthquake('Data/Southern Alaska Coast/grids/QCF3grid.xml'),
           'qcf4': uf.Earthquake('Data/Southern Alaska Coast/grids/QCF4grid.xml'),
           'qcf5': uf.Earthquake('Data/Southern Alaska Coast/grids/QCF5grid.xml'),
           'qcf6': uf.Earthquake('Data/Southern Alaska Coast/grids/QCF6grid.xml'),
           'qcf7': uf.Earthquake('Data/Southern Alaska Coast/grids/QCF7grid.xml'),
           'qcf8': uf.Earthquake('Data/Southern Alaska Coast/grids/QCF8grid.xml'),
           'qcf9': uf.Earthquake('Data/Southern Alaska Coast/grids/QCF9grid.xml'),
           'qcf10': uf.Earthquake('Data/Southern Alaska Coast/grids/QCF10grid.xml')}

# eqlist = [alu0, alu2, alu4, alu6, alu8, alu10, alu12]
# eqlabels = ['ALU0', 'ALU2', 'ALU4', 'ALU6', 'ALU8', 'ALU10', 'ALU12']
latlonlist = np.hstack((eq_dict['alu1'].lats, eq_dict['alu1'].lons))

for key in community_dict.keys():
    community_dict[key]['index'] = int(np.all(latlonlist == community_dict[key]['latlon'], axis=1).nonzero()[0][0])
    print(community_dict[key]['index'])
# print(ancindex)
for label, eq in eq_dict.items():
    for city in community_dict.values():
        if 'wt' not in city:
            city['wt'] = []
        city['wt'].append(float(np.around(eq.warning_times_s[city['index'], 0], decimals=1)))
        if 'pga' not in city:
            city['pga'] = []
        city['pga'].append(eq.pga[city['index'], 0])

with open('Data/Southern Alaska Coast/Community Data.json', 'w') as outfile:
    json.dump(community_dict, outfile)
