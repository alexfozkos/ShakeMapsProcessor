import math
import numpy as np
import UsefulFunctions as uf
import matplotlib

matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 16})


anccoords = [-149.9000, 61.2000]

alu0 = uf.Earthquake('Data/Southern Alaska Coast/grids/ALU1grid.xml')
alu2 = uf.Earthquake('Data/Southern Alaska Coast/grids/ALU3grid.xml')
alu4 = uf.Earthquake('Data/Southern Alaska Coast/grids/ALU5grid.xml')
alu6 = uf.Earthquake('Data/Southern Alaska Coast/grids/ALU7grid.xml')
alu8 = uf.Earthquake('Data/Southern Alaska Coast/grids/ALU9grid.xml')
alu10 = uf.Earthquake('Data/Southern Alaska Coast/grids/ALU11grid.xml')
alu12 = uf.Earthquake('Data/Southern Alaska Coast/grids/ALU13grid.xml')
eqlist = [alu0, alu2, alu4, alu6, alu8, alu10, alu12]
eqlabels = ['ALU0', 'ALU2', 'ALU4', 'ALU6', 'ALU8', 'ALU10', 'ALU12']
lonlatlist = np.hstack((alu0.lons, alu0.lats))
ancindex = np.all(lonlatlist == anccoords, axis=1).nonzero()[0][0]
# print(ancindex)


ancwt = []
ancpga = []
for eq in eqlist:
    ancwt.append(eq.warning_times_s[ancindex, 0])
    ancpga.append(eq.pga[ancindex, 0])
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(ancwt, marker='o', c='k', ls='--', label='Warning Time (s)')
ax1.set_xlabel('Scenario ID')
ax1.set_ylabel('Warning Time (s)', c='k')
ax1.set_xticks(range(len(eqlabels)))
ax1.set_xticklabels(eqlabels)
ax2.plot(ancpga, marker='o', c='r', label='PGA (%g)')
ax2.set_ylabel('PGA (%g)', c='r')
ax2.set_yscale('log')
plt.title('Scenario PGA and Warning Times for Anchorage')
# plt.legend()
plt.show()
