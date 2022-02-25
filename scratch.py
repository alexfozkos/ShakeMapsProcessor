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


sta_dist_e = np.array(
    [uf.getDistance(anc_05.event['lat'], anc_05.event['lon'], i, k)
     for (i, k) in zip(anc_05.ActiveBBs['lat'], anc_05.ActiveBBs['lon'])]
)
# get hypocentral distances, we care for arrival times
sta_dist_h = np.array(
    np.sqrt(np.power(sta_dist_e, 2) + anc_05.event['depth'] ** 2)
)
# sta_dist_col = sta_dist.reshape(sta_dist.shape[0], 1)

# Calculate P wave travel time to each station
sta_arr_p = sta_dist_h / anc_05.vel_p
# sta_arr_p_col = sta_arr_p.reshape(sta_arr_p.shape[0], 1)

# create array of columns of stations lons, lats, epicentral distances, and p arrival times
sta_list = np.vstack((anc_05.ActiveBBs['lon'], anc_05.ActiveBBs['lat'], sta_dist_e, sta_arr_p))
# turn into rows of data instead of columns (lon, lat, dist, p arrival)
sta_list = sta_list.transpose()
# sort the rows (each stations data) by the arrival times
sta_list = sta_list[sta_list[:, 3].argsort()]


plt.figure()
plt.scatter(anc_05.ActiveBBs['lon'], anc_05.ActiveBBs['lat'])
plt.scatter(anc_05.event['lon'], anc_05.event['lat'], c='r', marker='*')
colors = ['r','b','g','m']
for i in range(4):
    plt.plot([anc_05.event['lon'], sta_list[i, 0]], [anc_05.event['lat'], sta_list[i, 1]], c=colors[i])
plt.xlim(-151, -149.5)
plt.ylim(61, 62)
plt.show()
