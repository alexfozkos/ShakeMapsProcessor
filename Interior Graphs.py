import math
import numpy as np
import UsefulFunctions as uf
import json
import matplotlib
matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt
from MMILegend import mmimap, mmi_cmap, draw_colorbar

plt.rcParams.update({'font.size': 12})

eq_labels = ['Tintina','RSZ','MSZ','FSZ','SSZ','NF']
for i in range(1, 6):
    eq_labels.append(f'Denali_{i}')
for i in range(1, 3):
    eq_labels.append(f'CM_{i}')

with open('Data/Interior Crustal/Interior Community Data.json') as json_file:
    comm_dict = json.load(json_file)
print(len(comm_dict.keys()))

plt.rc('axes', titlesize=10, labelsize=8)
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)

fig, ax = plt.subplots(2, 5, figsize=(14, 8))
plots = {}
n = 0
grays = ['dimgray', 'silver', 'gainsboro']
for name, data in comm_dict.items():
    index = (n // 5, n % 5)
    ax[index].plot(data['wt'], marker='o', markersize=2, lw=1, c='k', ls='--', label='Warning time (s)')
    for i in range(0, 3):
        ax[index].axhline(i*10, lw=0.5, c=grays[i], ls=':')
    wt = ax[index].scatter(x=range(0,13),y=data['wt'], s=40, marker='o', c=data['mmi'], cmap=mmi_cmap,
                                   ls='--', label='Warning time (s)', vmin=0, vmax=10)
    ax[index].set_ylabel('Warning Time (s)')
    ax[index].set_title(name)
    ax[index].set_ylim(-20, 120)

    # ax2 = ax[n // 5, n % 5].twinx()
    # pga, = ax2.plot(data['pga'], marker='o', c='r', label='PGA (%g)', markersize=0.5, lw=0.3)
    # ax2.set_ylabel('PGA (%g)', c='r')
    # ax2.set_yscale('log')
    # ax[n // 5, n % 5].legend(handles=[wt, pga])
    n += 1
# plt.clim[1,8]
# plt.rc('xtick', labelsize=12)
# cbar_ax = fig.add_axes([0.15, 0.05, 0.7, 0.05])
# fig.colorbar(wt, cax=cbar_ax, orientation='horizontal',label='MMI')
plt.rc('xtick', labelsize=10)

draw_colorbar(fig, mmimap, None)
plt.text(0.48, 1.2, 'MMI', fontsize=16)
plt.suptitle('Newlist Community Scenario Data', fontsize=18)
plt.tight_layout(rect=[0, 0.1, 1, 0.99])
plt.savefig('Figures/Interior Crustal/Newlist Community Data colored markers.pdf')


# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.plot(ancwt, marker='o', c='k', ls='--', label='Warning Time (s)')
# ax1.set_xlabel('Scenario ID')
# ax1.set_ylabel('Warning Time (s)', c='k')
# ax1.set_xticks(range(len(eqlabels)))
# ax1.set_xticklabels(eqlabels)
# ax2.plot(ancpga, marker='o', c='r', label='PGA (%g)')
# ax2.set_ylabel('PGA (%g)', c='r')
# ax2.set_yscale('log')
# plt.title('Scenario PGA and Warning Times for Anchorage')
# # plt.legend()
# plt.show()
