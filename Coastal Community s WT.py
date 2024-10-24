import json
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from MMILegend import mmimap, mmi_cmap, draw_colorbar
import numpy as np

# load in community data
with open('Data/Southern Alaska Coast/Community Data.json') as json_file:
    comm_dict = json.load(json_file)

print(comm_dict.keys())

community = 'Whittier'
whittier = comm_dict[community]
scenarios = whittier['scenarios']
print(scenarios.keys())
print(scenarios['1'].keys())

height = 0.5
lw = 0.5
ytick_labels = []
mmi_min = 0
mmi_max = 10
# figure_fname = f'Community vs WT Zoom MMI {mmi_min}+.png'
# title = f'MMI {mmi_min} - {mmi_max}'
figure_fname = f'Community vs WT Zoom cbar pga.png'
title = 'Coastal - All Communities'
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
comm_n_add = 0
for community in comm_dict.keys():
    s_ns = []
    scenarios = comm_dict[community]['scenarios']
    wt_mins = np.array([])
    wt_maxs = np.array([])
    mmis = np.array([])
    pgas = np.array([])
    e_dists = np.array([])
    for i in range(1, 26):
        if mmi_min <= scenarios[f'{i}']['mmi'] < mmi_max:
            wt_mins = np.append(wt_mins, scenarios[f'{i}']['wt_min'])
            wt_maxs = np.append(wt_maxs, scenarios[f'{i}']['wt_max'])
            mmis = np.append(mmis, scenarios[f'{i}']['mmi'])
            e_dists = np.append(e_dists, scenarios[f'{i}']['e_dist'])
            pgas = np.append(pgas, scenarios[f'{i}']['pga'])
            s_ns.append(i)
        else:
            continue
    comm_n = np.ones(shape=(len(s_ns),)) + comm_n_add

    # wt = ax.scatter(wt_mins, comm_n, s=0, marker='o', c=pgas, cmap='viridis',
    #                 vmin=0, vmax=100, zorder=0, linewidth=0, edgecolor='k', alpha=1)

    color = np.array([mmi_cmap(i / 10) for i in mmis])
    # color = np.array([])
    # https://matplotlib.org/stable/gallery/statistics/errorbars_and_boxes.html#sphx-glr-gallery-statistics-errorbars-and-boxes-py
    # code for plotting rectangle ranges of warning time
    wtboxes = [Rectangle((x, y - height / 2), width, height) for x, y, width in
               zip(wt_mins, comm_n, np.array(wt_maxs) - np.array(wt_mins))]
    pc = PatchCollection(wtboxes, linewidth=lw, edgecolor='k', alpha=0.8, norm=colors.LogNorm())
    pc.set_array(pgas)
    pc.set_clim(1, 100)
    ax.add_collection(pc)
    # plot scenario nums
    midpoints = wt_mins + (wt_maxs-wt_mins)/2
    for i in range(len(s_ns)):
        if midpoints[i] < 120:
            ax.text(midpoints[i],  comm_n[i]+0.13, s_ns[i], c='gray', fontsize=6, ha='center', va='bottom', alpha=0.75)

    ytick_labels.append(community)
    print(np.max(pgas))
    comm_n_add += 1
ax.scatter(x=0, y=len(comm_dict.keys()), s=0, c='k')
ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=14)

ax.set_title(f'{title}', fontsize=14)
# ax.set_ylim(ymax=27)
# ax.set_xticks([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25])
ax.set_yticks(range(1, len(comm_dict.keys()) + 1))
ax.set_yticklabels(ytick_labels)
ax.set_xlim(xmin=-10, xmax=120)
ax.axvline(0, lw=1, c='k', zorder=0, )

ax.grid(alpha=0.4, zorder=0, axis='y')

# cbar_ax = fig.add_axes([0.92, 0.2, 0.03, 0.6])
# cbar_ax.tick_params(labelsize=12)
# cb = fig.colorbar(wt, cax=cbar_ax, orientation='vertical', label='MMI')
# cb.set_label(label='MMI', fontsize=14)
plt.rc('xtick', labelsize=14)

# fig.text(0.51, 0.05, 'Epicentral Distance', ha='center', va='center', fontsize=18)
# fig.text(0.04, 0.5, 'Warning Time (s)', ha='center', va='center', rotation='vertical', fontsize=18)
ax.set_xlabel('Warning Time (s)', fontsize=16)
# plt.tight_layout()
fig.colorbar(pc, label='PGA (%g)', shrink=0.4, pad=0.01)
plt.savefig(f'Figures/CoastalScenarios/{figure_fname}', bbox_inches='tight')

# print(wt_maxs-wt_mins)
