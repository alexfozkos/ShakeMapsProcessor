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

community = 'Whittier'
whittier = comm_dict[community]
scenarios = whittier['scenarios']
print(scenarios.keys())
print(scenarios['1'].keys())

height = 0.5
lw = 0.5

for s_n in range(1, 26):
    ytick_labels = []
    comm_n = 1
    figure_fname = f'Scenario {s_n}.png'
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    for community in comm_dict.keys():
        scenarios = comm_dict[community]['scenarios']

        wt_min = scenarios[f'{s_n}']['wt_min']
        wt_max = scenarios[f'{s_n}']['wt_max']
        mmi = [scenarios[f'{s_n}']['mmi']]
        e_dist = scenarios[f'{s_n}']['e_dist']

        wt = ax.scatter(wt_min, comm_n, s=0, marker='o', c=mmi, cmap=mmi_cmap,
                        vmin=0, vmax=10, zorder=0, linewidth=0, edgecolor='k', alpha=1)

        color = np.array([mmi_cmap(i / 10) for i in mmi])

        # https://matplotlib.org/stable/gallery/statistics/errorbars_and_boxes.html#sphx-glr-gallery-statistics-errorbars-and-boxes-py
        # code for plotting rectangle ranges of warning time
        wtbox = Rectangle((wt_min, comm_n - height / 2), wt_max-wt_min, height,
                          facecolor=color, linewidth=lw, edgecolor='k', alpha=0.8)

        # pc = PatchCollection(wtboxes, color=color, cmap=mmi_cmap, linewidth=lw, edgecolor='k', alpha=0.8)
        ax.add_patch(wtbox)
        # plot scenario nums
        midpoint = wt_min + (wt_max-wt_min)/2
        ax.text(midpoint, comm_n+0.13, s_n, c='gray', fontsize=6, ha='center', va='bottom', alpha=0.75)

        ytick_labels.append(community)
        comm_n += 1

    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=12)

    ax.set_title('All communities', fontsize=14)
    # ax.set_ylim(0 - 5, 120)
    # ax.set_xticks([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25])
    ax.set_yticks(range(1, len(comm_dict.keys()) + 1))
    ax.set_yticklabels(ytick_labels)
    ax.set_xlim(xmin=-10, xmax=120)
    ax.axvline(0, lw=1, c='k', zorder=0, )

    ax.grid(alpha=0.4, zorder=0, axis='y')

    cbar_ax = fig.add_axes([0.92, 0.2, 0.03, 0.6])
    cbar_ax.tick_params(labelsize=12)
    cb = fig.colorbar(wt, cax=cbar_ax, orientation='vertical', label='MMI')
    cb.set_label(label='MMI', fontsize=14)
    plt.rc('xtick', labelsize=14)

    # fig.text(0.51, 0.05, 'Epicentral Distance', ha='center', va='center', fontsize=18)
    # fig.text(0.04, 0.5, 'Warning Time (s)', ha='center', va='center', rotation='vertical', fontsize=18)
    ax.set_xlabel('Warning Time (s)')

    # plt.tight_layout()
    plt.savefig(f'Figures/CoastalScenarios/Comm v WT by Scenario/{figure_fname}')
    plt.close(fig)
    # print(wt_maxs-wt_mins)
