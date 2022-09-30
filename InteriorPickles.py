import math
import numpy as np
import UsefulFunctions as uf
import matplotlib
import json
matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 16})

grays = ['dimgray', 'silver', 'gainsboro']
eq_labels = ['Tintina','RSZ','MSZ','FSZ','SSZ','NF']
for i in range(1, 6):
    eq_labels.append(f'Denali_{i}')
for i in range(1, 3):
    eq_labels.append(f'CM_{i}')

with open('Data/Interior Crustal/Interior Community Data.json') as json_file:
    comm_dict = json.load(json_file)
print(len(comm_dict.keys()))
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

plt.figure()
for i in range(0, 3):
    plt.axhline(i * 10, lw=0.5, c=grays[i], ls=':')

for k, v in eq_dict.items():
    x, y = uf.createPolygon(v.mmi, v.warning_times_s, xscale='lin')
    plt.plot(x, y, c='gray', alpha=0.8)


plt.ylabel('Warning Time (s)')
plt.xlabel('MMI')
plt.title('Interior Scenarios WT vs MMI')
plt.show()
