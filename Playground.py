import os
import UsefulFunctions as uf
import numpy as np
from matplotlib import pyplot as plt
import collections

eq = uf.Earthquake()

mmi_min = np.min(eq.mmi)
mmi_max = np.max(eq.mmi)

n = 50
# Create array of warning times, epicentral distances, and mmi for each point
points = np.hstack((eq.warning_times[::n], eq.distances[::n], eq.mmi[::n]))
# Sort the points by Distance
points = points[np.argsort(points[:, 1])]
# Create a dictionary where key=mmi, each value is an vertically stacked array of [warning time, distance]
# for each point
point_dict = {}

for i in points:
    key = i[2] * 10 / 10
    if key not in point_dict.keys():
        point_dict[key] = np.array(i[:2])
        pass
    point_dict[key] = np.vstack((point_dict[key], i[:2]))

#Sorts the dictionary keys by mmi, decreasing (highest mmi keys first)
point_dict = collections.OrderedDict(reversed(sorted(point_dict.items())))

# various variables for playing with data representation
j = 0
k = 1
# create a plot for the data, then plot the data by each mmi group, moving points vertically around the real plot
# using a cosine function to try and spread the groups out for better visualization
norm = plt.Normalize(mmi_min, mmi_max)
fig, axs = plt.subplots(1, figsize=(12, 12))
axs.plot(points[:, 1], points[:, 0], c='cyan', lw=0.4, ls='--')
for mmi in point_dict.keys():
    axs.scatter(x=(point_dict[mmi][:, 1]),
                y=point_dict[mmi][:, 0] + 3*np.cos(j*np.pi/3),
                s=0.2,
                label=mmi,
                c=[mmi for x in point_dict[mmi][:, 0]],
                cmap='inferno',
                norm=norm,
                )
    j += 1
    # k = -k

smap = plt.cm.ScalarMappable(cmap='inferno', norm=norm)
cbar = fig.colorbar(smap, ax=axs, fraction=0.1, shrink=0.8, label='MMI')
plt.xlabel('Epicentral Distance (km)')
plt.ylabel('Warning Time (s)')
# plt.legend()
plt.savefig('Figures/WTvDist_funky.png')
