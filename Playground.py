import UsefulFunctions as uf
import numpy as np
from matplotlib import pyplot as plt
import collections

eq = uf.Earthquake()

mmi_min = np.min(eq.mmi)
mmi_max = np.max(eq.mmi)

points = np.hstack((eq.warning_times, eq.distances, eq.mmi))
points = points[np.argsort(points[:, 1])]

point_dict = {}

for i in points:
    key = i[2] * 10 / 10
    if key not in point_dict.keys():
        point_dict[key] = np.array(i[:2])
        pass
    point_dict[key] = np.vstack((point_dict[key], i[:2]))

point_dict = collections.OrderedDict(reversed(sorted(point_dict.items())))

print(list(point_dict[5.6][:, 1]))
print(point_dict.keys())

j = 0
k = 1
norm = plt.Normalize(mmi_min, mmi_max)
fig, axs = plt.subplots(1)
axs.plot(points[:, 1], points[:, 0], c='cyan', lw=0.4, ls='--')
for mmi in point_dict.keys():
    axs.scatter(x=(point_dict[mmi][:, 1]),
                y=point_dict[mmi][:, 0] + 3*np.cos(j*np.pi/3),
                s=0.6,
                label=mmi,
                c=[mmi for x in point_dict[mmi][:, 0]],
                cmap='inferno',
                norm=norm,
                )
    j += 1
    # k = -k

smap = plt.cm.ScalarMappable(cmap='inferno', norm=norm)
cbar = fig.colorbar(smap, ax=axs, fraction=0.1, shrink=0.8)
plt.xlabel('Epicentral Distance (km)')
plt.ylabel('Warning Time (s)')
# plt.legend()
plt.show()
