import math
import numpy as np
import UsefulFunctions as uf
import matplotlib
import json
matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt
from matplotlib import cm, colors

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


my_cmap = cm.winter
my_norm = colors.Normalize(vmin=1, vmax=13)

fig, ax = plt.subplots(figsize=(8, 6))
warn_colors = ['maroon', 'orange', 'yellow']
for i in range(0, 3):
    ax.axhline(i * 10, lw=1.5, c=warn_colors[i], ls=':', zorder=0, label='%i s' % (i * 10))

ii=0
for k, v in eq_dict.items():
    mmi = v.mmi
    wt = v.warning_times_s
    wt_means = []
    wt_medians = []
    mmi_vals = np.arange(mmi.min(), mmi.max() + 0.1, 0.1)
    for p in mmi_vals:
        mask = np.isclose(mmi, p)
        wt_means.append(np.mean(wt[mask]))
        wt_medians.append(np.median(wt[mask]))

    # x, y = uf.createPolygon(v.mmi, v.warning_times_s, xscale='lin')
    # ax.plot(x, y, c='dimgray', alpha=0.9)
    # ax.plot(mmi_vals, wt_means, lw=2, marker='^', markersize=3, c='g', label='Warning Time Means', alpha=0.9)
    ax.plot(mmi_vals, wt_medians, lw=4, c=my_cmap(my_norm(ii)), label='Warning Time Medians', alpha=0.7)
    ii+=0

ax.set_ylabel('Warning Time (s)')
ax.set_xlabel('MMI')
# plt.title('Interior Scenarios WT vs MMI')
plt.savefig('Figures/Interior Crustal/pickles.png', dpi=700)
plt.savefig('Figures/Interior Crustal/pickles.pdf', dpi=700)

