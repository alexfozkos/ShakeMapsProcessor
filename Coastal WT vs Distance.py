import json
from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from MMILegend import mmimap, mmi_cmap, draw_colorbar
import numpy as np

# load in community data
with open('Data/Southern Alaska Coast/Community Data.json') as json_file:
    comm_dict = json.load(json_file)

print(comm_dict.keys())

figure_fname = 'Wt vs Distance.png'
community = 'Whittier'
whittier = comm_dict[community]
scenarios = whittier['scenarios']
print(scenarios.keys())
print(scenarios['1'].keys())

width = 10
lw = 0.5
figure_fname = 'Wt vs Distance.png'

fig, ax = plt.subplots(1, 1, figsize=(6, 6))

for community in comm_dict.keys():
    scenarios = comm_dict[community]['scenarios']
    wt_mins = np.array([])
    wt_maxs = np.array([])
    mmis = np.array([])
    e_dists = np.array([])
    for i in range(1, 26):
        wt_mins = np.append(wt_mins, scenarios[f'{i}']['wt_min'])
        wt_maxs = np.append(wt_maxs, scenarios[f'{i}']['wt_max'])
        mmis = np.append(mmis, scenarios[f'{i}']['mmi'])
        e_dists = np.append(e_dists, scenarios[f'{i}']['e_dist'])

    print(e_dists)

    wt = ax.scatter(e_dists, wt_mins, s=0, marker='o', c=mmis, cmap=mmi_cmap,
                    vmin=0, vmax=10, zorder=0, linewidth=0, edgecolor='k', alpha=1)
    color = np.array([mmi_cmap(i / 10) for i in mmis])

    # https://matplotlib.org/stable/gallery/statistics/errorbars_and_boxes.html#sphx-glr-gallery-statistics-errorbars-and-boxes-py
    # code for plotting rectangle ranges of warning time
    wtboxes = [Rectangle((x - width / 2, y), width, height) for x, y, height in
               zip(e_dists, wt_mins, np.array(wt_maxs) - np.array(wt_mins))]
    pc = PatchCollection(wtboxes, color=color, cmap=mmi_cmap, linewidth=lw, edgecolor='k')
    ax.add_collection(pc)

ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=12)

ax.set_title('All communities', fontsize=14)
ax.set_ylim(0 - 5, 120)
# ax.set_xticks([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25])
ax.set_xlim(0, 500)
ax.axhline(0, lw=1, c='k', zorder=0, )

ax.grid(alpha=0.4, zorder=0, axis='y')

cbar_ax = fig.add_axes([0.92, 0.2, 0.03, 0.6])
cbar_ax.tick_params(labelsize=12)
cb = fig.colorbar(wt, cax=cbar_ax, orientation='vertical', label='MMI')
cb.set_label(label='MMI', fontsize=14)
plt.rc('xtick', labelsize=14)

fig.text(0.51, 0.05, 'Epicentral Distance', ha='center', va='center', fontsize=18)
fig.text(0.04, 0.5, 'Warning Time (s)', ha='center', va='center', rotation='vertical', fontsize=18)

plt.savefig(f'Figures/CoastalScenarios/{figure_fname}')

# print(wt_maxs-wt_mins)
