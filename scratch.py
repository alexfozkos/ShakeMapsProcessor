import math
import numpy as np
import UsefulFunctions as uf
import matplotlib
matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt

qcf1 = uf.Earthquake('Data/Southern Alaska Coast/grids/QCF1grid.xml')
qcf1_man = uf.Earthquake('Data/Southern Alaska Coast/grids/QCF1man_grid.xml')
eqlist_mini = [qcf1, qcf1_man]
colors = ['r', 'g', 'b']
fig, ax = plt.subplots(figsize=(8, 6))
fig.suptitle('QCF1 Automatic vs Manual GMPE')
eqlabels_mini = ['Automatic', 'Manual']

# for j in np.linspace(-10, 110, num=13):
#     ax.axhline(j, c='silver', lw=0.5)
for i in range(len(eqlist_mini)):
    eq = eqlist_mini[i]
    # x, y = uf.createPolygon(eq.pga, eq.distances_epi, xscale='lin')
    ax.scatter(eq.pga, eq.distances_epi, s=1, c=colors[i], label=eqlabels_mini[i])
    # ax[i].plot(x, y, c=colors[i], alpha=0.6)
    # ax.fill(y, x, c=colors[i], alpha=0.5, label=eqlabels_mini[i])
# ax.axhline(0, c='k', lw=1)
# ax.set_xscale('log')
# ax.invert_xaxis()
# ax.set_xlim(2.5, 8)
# ax.set_ylim(-15, 120)
ax.set_ylabel('PGA (%g)')
ax.set_xlabel('Distance (km)')
ax.set_yscale('log')
plt.legend(loc='upper right')
# plt.tight_layout(rect=(0, 0, 1, 0.99))
plt.savefig('Figures/test.png')
plt.show()
