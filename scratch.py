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
anc_50 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid50.xml')
anc_125 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid125.xml')

eq = [anc_05, anc_50, anc_125]
plt.figure()
colors = ['r', 'g', 'b']
# for i in range(3):
#     plt.scatter(eq[i].pga, eq[i].arrivals_s, c=colors[i], s=25)
plt.scatter(-anc_50.pga, anc_50.arrivals_s)
plt.axhline(anc_50.detection_time, ls='--',c='k')
plt.axhline(anc_50.detection_time+uf.Earthquake.TTP, ls=':', c='k')
plt.ylim(0,60)
plt.savefig('ahhh.png')
plt.xlabel('pga')
plt.ylabel('seconds after origin')
plt.show()
