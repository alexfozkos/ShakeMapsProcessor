import numpy as np
import UsefulFunctions as uf
from matplotlib import pyplot as plt

eq = uf.Earthquake()

m, b = np.polyfit(eq.mmi, (eq.pga), 1)

fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(16, 16))

ax1.plot(eq.distances, eq.warning_times)
ax1.set(xlabel='distance (m)', ylabel='warning time (s)')

ax2.scatter(eq.arrivals_s, eq.mmi, s=0.5)
ax2.set(xlabel='S arrival time (s)', ylabel='MMI')

ax3.plot(eq.mmi, eq.pga, 'bo', eq.mmi, m * eq.mmi + b, '--k')
ax3.set(xlabel='MMI', ylabel='PGA (%g)')

fig.tight_layout()
plt.savefig('tester.png')
