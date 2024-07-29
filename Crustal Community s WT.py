import json
from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from MMILegend import mmimap, mmi_cmap, draw_colorbar
import numpy as np

# load in community data
with open('Data/Interior Crustal/Community Data.json') as json_file:
    comm_dict = json.load(json_file)

print(comm_dict.keys())

height = 0.5
lw = 0.5
xmax = 60
xmin = -15
ytick_labels = []
mmi_min = 0
mmi_max = 10
# figure_fname = f'Community vs WT Zoom MMI {mmi_min} to {mmi_max}.png'
# title = f'MMI {mmi_min} - {mmi_max}'
figure_fname = f'Community vs WT Zoom.png'
title = 'Crustal - All Communities'
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
comm_n_add = len(comm_dict.keys())
for community in comm_dict.keys():
    s_ns = []
    scenarios = comm_dict[community]['scenarios']
    wt_mins = np.array([])
    wt_maxs = np.array([])
    mmis = np.array([])
    e_dists = np.array([])
    for i in range(1, len(scenarios.keys())):
        if mmi_min <= scenarios[f'{i}']['mmi'] < mmi_max:
            wt_mins = np.append(wt_mins, scenarios[f'{i}']['wt_min'])
            wt_maxs = np.append(wt_maxs, scenarios[f'{i}']['wt_max'])
            mmis = np.append(mmis, scenarios[f'{i}']['mmi'])
            e_dists = np.append(e_dists, scenarios[f'{i}']['e_dist'])
            s_ns.append(i)
        else:
            continue
    comm_n = np.ones(shape=(len(s_ns),)) * comm_n_add

    wt = ax.scatter(wt_mins, comm_n, s=0, marker='o', c=mmis, cmap=mmi_cmap,
                    vmin=0, vmax=10, zorder=0, linewidth=0, edgecolor='k', alpha=1)

    color = np.array([mmi_cmap(i / 10) for i in mmis])

    # https://matplotlib.org/stable/gallery/statistics/errorbars_and_boxes.html#sphx-glr-gallery-statistics-errorbars-and-boxes-py
    # code for plotting rectangle ranges of warning time
    wtboxes = [Rectangle((x, y - height / 2), width, height) for x, y, width in
               zip(wt_mins, comm_n, np.array(wt_maxs) - np.array(wt_mins))]
    pc = PatchCollection(wtboxes, color=color, cmap=mmi_cmap, linewidth=lw, edgecolor='k', alpha=0.8)
    ax.add_collection(pc)
    # plot scenario nums
    midpoints = wt_mins + (wt_maxs-wt_mins)/2
    for i in range(len(s_ns)):
        if midpoints[i] < xmax:
            ax.text(midpoints[i],  comm_n[i]+0.13, s_ns[i], c='gray', fontsize=6, ha='center', va='bottom', alpha=0.75)

    ytick_labels.append(community)
    comm_n_add -= 1

ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=14)

ax.set_title(f'{title}', fontsize=14)
# ax.set_ylim(0 - 5, 120)
# ax.set_xticks([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25])
ax.set_yticks(range(1, len(comm_dict.keys()) + 1))
ax.set_yticklabels(ytick_labels[::-1])
ax.set_xlim(xmin=xmin, xmax=xmax)
ax.axvline(0, lw=1, c='k', zorder=0, )

ax.grid(alpha=0.4, zorder=0, axis='y')

# cbar_ax = fig.add_axes([0.8, 0.55, 0.03, 0.4])
#
# cbar_ax.tick_params(labelsize=10)
# cb = fig.colorbar(wt, cax=cbar_ax, orientation='vertical', label='MMI')
# cb.set_label(label='MMI', fontsize=10)
plt.rc('xtick', labelsize=14)

# fig.text(0.51, 0.05, 'Epicentral Distance', ha='center', va='center', fontsize=18)
# fig.text(0.04, 0.5, 'Warning Time (s)', ha='center', va='center', rotation='vertical', fontsize=18)
ax.set_xlabel('Warning Time (s)')

# plt.tight_layout()
plt.savefig(f'Figures/Interior Crustal/{figure_fname}',  bbox_inches='tight')


# print(wt_maxs-wt_mins)
