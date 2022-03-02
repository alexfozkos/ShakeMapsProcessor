import math
import numpy as np
import UsefulFunctions as uf
import matplotlib
matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt


# x = np.linspace(0, 2*np.pi, num=9)
# plt.figure()
# plt.scatter(x, np.sin(x))

anc_05 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid05.xml')
# anc_50 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid50.xml')
# anc_125 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid125.xml')

# eq = [anc_05, anc_50, anc_125]
# plt.figure()
# colors = ['r', 'g', 'b']
# # for i in range(3):
# #     plt.scatter(eq[i].pga, eq[i].arrivals_s, c=colors[i], s=25)
# plt.scatter(-anc_50.pga, anc_50.arrivals_s)
# plt.axhline(anc_50.detection_time, ls='--',c='k')
# plt.axhline(anc_50.detection_time+uf.Earthquake.TTP, ls=':', c='k')
# plt.ylim(0,60)
# plt.savefig('ahhh.png')
# plt.xlabel('pga')
# plt.ylabel('seconds after origin')
# plt.show()

data = np.hstack((anc_05.pga, anc_05.warning_times_s))
data = data[data[:, 0].argsort()]
data = data[::-1]
pga_sorted = data[:, 0]
wt_sorted = data[:, 1]
n = 250
# pga_space = np.arange(start=anc_05.pga.min(), stop=(anc_05.pga.max() + n), step=n)
pga_space = np.logspace(-4, 2, num=n)
pga_space = pga_space[::-1]
print(pga_space[-1::-10])
maxmins = np.zeros((2, 1))
pga_mids = np.array([])
for i in range(pga_space.shape[0] - 1):
    slice_index = np.where((pga_sorted < pga_space[i]) & (pga_sorted >= pga_space[i + 1]), [True], [False])
    wt_slice = wt_sorted[slice_index]
    if np.size(wt_slice) == 0:
        continue
    topbot = np.array([[np.max(wt_slice)], [np.min(wt_slice)]])
    maxmins = np.hstack((maxmins, topbot))
    midway = np.exp((np.log(pga_space[i]) + np.log(pga_space[i+1]))/2)
    # pga_mids = np.append(pga_mids, (pga_space[i]+pga_space[i+1])/2)
    pga_mids = np.append(pga_mids, midway)

maxmins = maxmins[:, 1:]  # pop off that inital 0 column
wt_maxes = maxmins[0, :]
wt_mins = maxmins[1, :]
wt_mins = wt_mins[::-1]  # reverse mins so we can draw from left to right, up thorugh the maxes and back  down left through the mins
wt_points = np.append(wt_maxes, wt_mins)
pga_mids = np.append(pga_mids, pga_mids[::-1])  # add the same mid points but backwards for the mins
pga_mids = np.append(pga_mids, pga_mids[0])  # pad these two at the end to create a closed polygon
wt_points = np.append(wt_points, wt_points[0])

print(pga_sorted.max(), pga_sorted.min())
print(pga_mids.max(), pga_mids.min())
print(pga_space.max(), pga_space.min())
fig, ax = plt.subplots(1)
ax.scatter(anc_05.pga, anc_05.warning_times_s, c='r', alpha=0.1)
ax.plot(pga_mids, wt_points, c='k')
plt.fill(pga_mids, wt_points, c='c')
ax.invert_xaxis()
ax.set_xscale('log')
plt.show()
