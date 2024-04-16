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
for i in range(14, 16):
    eq_labels.append(f'CSE{i}')
for i in range(16, 26):
    eq_labels.append(f'QCF{i}')

with open('Data/Southern Alaska Coast/Old Community Data.json') as json_file:
    comm_dict = json.load(json_file)
# print(len(comm_dict.keys()))

plt.rc('axes', titlesize=10, labelsize=8)
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)

fig, ax = plt.subplots(2, 3, figsize=(10, 8))
plots = {}
wt_min = 100
wt_max = 0
warn_colors = ['maroon', 'orange', 'yellow']

for name, data in comm_dict.items():
    if name in ['Kodiak', 'Seward', 'Valdez', 'Juneau', 'Sitka', 'Ketchikan']:
        if min(data['wt']) < wt_min:
            wt_min = min(data['wt'])
        if max(data['wt']) > wt_max:
            wt_max = max(data['wt'])
    else:
        continue

for name, data in comm_dict.items():
    if name == 'Kodiak':
        index = (0, 0)
    elif name == 'Seward':
        index = (0, 1)
    elif name == 'Valdez':
        index = (0, 2)
    elif name == 'Juneau':
        index = (1, 0)
    elif name == 'Sitka':
        index = (1, 1)
    elif name == 'Ketchikan':
        index = (1, 2)
    else:
        continue
    for i in range(0, 3):
        ax[index].axhline(i * 10, lw=1.5, c=warn_colors[i], ls=':', zorder=0, label='%i s' % (i * 10))
    ax[index].scatter(range(1, 26), data['wt'], marker='o', s=60, c='k', zorder=3)
    wt = ax[index].scatter(range(1, 26), data['wt'], s=40, marker='o', c=data['mmi'], cmap=mmi_cmap,
                           vmin=0, vmax=10, zorder=4)
    ax[index].set_title(name, fontsize=12)
    ax[index].set_ylim(wt_min-5, 120)
    ax[index].set_xticks([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25])
    if name == 'Kodiak':
        ax[index].legend(loc='upper right', fontsize=10)
# plt.clim[1,8]
# plt.rc('xtick', labelsize=12)
cbar_ax = fig.add_axes([0.92, 0.2, 0.03, 0.6])
fig.colorbar(wt, cax=cbar_ax, orientation='vertical', label='MMI')
# fig.colorbar(wt, cax=cbar_ax, orientation='horizontal', label='MMI')
plt.rc('xtick', labelsize=12)

# draw_colorbar(fig, mmimap, None)
# plt.text(0.48, 1.2, 'MMI', fontsize=16)
# plt.suptitle('Newlist Community Scenario Data', fontsize=18)
fig.text(0.51, 0.06, 'Scenario Number', ha='center', va='center',fontsize=14)
fig.text(0.07, 0.5, 'Warning Time (s)', ha='center', va='center', rotation='vertical',fontsize=14)
# plt.tight_layout(rect=[0.07, 0.04, 0.95, 1])
plt.savefig('Figures/CoastalScenarios/Coastal Community Data_notitle.pdf')
plt.savefig('Figures/CoastalScenarios/Coastal Community Data_notitle.png', dpi=700)

