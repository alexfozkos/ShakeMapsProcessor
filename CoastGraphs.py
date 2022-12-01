import math
import numpy as np
import UsefulFunctions as uf
import json
import matplotlib
matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt
from MMILegend import mmimap, mmi_cmap, draw_colorbar

plt.rcParams.update({'font.size': 12})

eq_labels = []
for i in range(1, 14):
    eq_labels.append(f'ALU{i}')
for i in range(1, 3):
    eq_labels.append(f'CSE{i}')
for i in range(1, 11):
    eq_labels.append(f'QCF{i}')

with open('Data/Southern Alaska Coast/Community Data.json') as json_file:
    comm_dict = json.load(json_file)
# print(len(comm_dict.keys()))

plt.rc('axes', titlesize=10, labelsize=8)
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)

fig, ax = plt.subplots(3, 5, figsize=(14, 8))
plots = {}
n = 0
for name, data in comm_dict.items():
    # wt, = ax[n // 5, n % 5].plot(range(1, 26), data['wt'], marker='o', markersize=0.5, lw=1, c='k', ls='--', label='Warning time (s)')
    ax[n // 5, n % 5].plot(range(1, 26), data['wt'], marker='o', markersize=2, lw=1, c='k', ls='--', label='Warning time (s)')
    wt = ax[n // 5, n % 5].scatter(range(1, 26), data['wt'], s=40, marker='o', c=data['mmi'], cmap=mmi_cmap,
                                   ls='--', label='Warning time (s)', vmin=0, vmax=10)
    ax[n // 5, n % 5].set_ylabel('Warning Time (s)')
    ax[n // 5, n % 5].set_title(name)
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
# plt.suptitle('Newlist Community Scenario Data', fontsize=18)
plt.tight_layout(rect=[0, 0.1, 1, 0.99])
plt.savefig('Figures/CoastalScenarios/Coastal Community Data.pdf')
plt.savefig('Figures/CoastalScenarios/Coastal Community Data.png', dpi=700)

