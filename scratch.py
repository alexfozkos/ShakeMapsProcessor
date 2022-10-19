import math
import numpy as np
import pandas as pd
import UsefulFunctions as uf
import json
import matplotlib
from MMILegend import mmimap, mmi_cmap, draw_colorbar

matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt
from MMILegend import mmimap, mmi_cmap, draw_colorbar

plt.rcParams.update({'font.size': 12})

crst_hypocenters = pd.read_csv('Data/Interior Crustal/Crustal_Hypocenters.txt', delimiter='\t',
                               names=['lon', 'lat', 'depth', 'dip', 'strike', 'name'])

eq_labels = ['Tintina', 'RSZ', 'MSZ', 'FSZ', 'SSZ', 'NF']
for i in range(1, 6):
    eq_labels.append(f'Denali_{i}')
for i in range(1, 3):
    eq_labels.append(f'CM_{i}')

with open('Data/Interior Crustal/Interior Community Data.json') as json_file:
    comm_dict = json.load(json_file)
print(len(comm_dict.keys()))

# plt.rc('axes', titlesize=10, labelsize=8)
# plt.rc('xtick', labelsize=6)
# plt.rc('ytick', labelsize=6)

markers = 'o^v12spP*h+xD'
fig, ax = plt.subplots(figsize=(6,6))

for row in crst_hypocenters.iterrows():
    distances = []
    mmis = []
    wts = []
    for name, data in comm_dict.items():
        distances.append(uf.getDistance(row[1]['lat'], row[1]['lon'], data['latlon'][0], data['latlon'][1]))
        mmis.append(data['mmi'][row[0]])
        wts.append(data['wt'][row[0]])

    ax.scatter(distances, wts, c=mmis, cmap=mmi_cmap, marker='o', label=row[1]['name'])
ax.axhline(0, ls=':', c='k', alpha=.5)
ax.set_xlabel('Epicentral Distance (km)')
ax.set_ylabel('Warning Times (s)')
ax.set_title('Distance vs warning times for Crustal Quakes')
draw_colorbar(fig, mmimap, None)
plt.tight_layout()
plt.savefig('Figures/misc/test.pdf')
