import numpy as np
import UsefulFunctions as uf
from matplotlib import pyplot as plt

urls = ['', '', '']
eq = uf.Earthquake()

# m, b = np.polyfit(eq.mmi, (eq.pga), 1)

# fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(16, 16))
#
# ax1.plot(eq.distances, eq.warning_times)
# ax1.set(xlabel='distance (m)', ylabel='warning time (s)')
#
# ax2.scatter(eq.arrivals_s, eq.mmi, s=0.5)
# ax2.set(xlabel='S arrival time (s)', ylabel='MMI')
#
# ax3.plot(eq.mmi, eq.pga, 'bo', eq.mmi, m * eq.mmi + b, '--k')
# ax3.set(xlabel='MMI', ylabel='PGA (%g)')
#
# fig.tight_layout()
# plt.savefig('tester.png')

# plt.clf()
# vals = np.hstack((eq.distances, eq.warning_times, eq.mmi))
# vals_sorted = vals[np.argsort(vals[:, 2])]

fig, (ax1, ax2) = plt.subplots(2, figsize=(16,16))

z1 = ax1.scatter(eq.distances, eq.warning_times, s=0.5, c=eq.mmi, cmap='rainbow')
ax1.set_xlabel('Distance from Epicenter (km)')
ax1.set_ylabel('Warning time, before S wave arrivals (s)')
plt.colorbar(z1, label='MMI', ax=ax1)

z2 = ax2.scatter(eq.distances, eq.warning_times, s=0.5, c=eq.pga, cmap='rainbow')
ax2.set_xlabel('Distance from Epicenter (km)')
ax2.set_ylabel('Warning time, before S wave arrivals (s)')
plt.colorbar(z2, label='PGA (%g)', ax=ax2)

fig.tight_layout()
plt.savefig('Warning Times vs Epicentral Distance')
