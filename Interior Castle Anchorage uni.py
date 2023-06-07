import UsefulFunctions as uf
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

castle_2 = uf.Earthquake('Data/Interior Crustal/grids/Castle_2.xml')
castle_2_sw = uf.Earthquake('Data/Interior Crustal/grids/Castle_2_SW.xml')
castle_2_ne = uf.Earthquake('Data/Interior Crustal/grids/Castle_2_NE.xml')
eqs = [castle_2_ne, castle_2, castle_2_sw]

latlon = [61.2167, -149.8936]
lat = 61.2167
lon = -149.8936
subtracted_list = np.hstack((castle_2.lats - lat, castle_2.lons - lon))
ind = np.nanargmin(np.sum(subtracted_list ** 2, axis=1))
for eq in eqs:
    print(f'''
Detection time: {eq.detection_time}
Alert time: {eq.alert_time}
warning time fast: {eq.warning_times_s[ind]}
warning time slow: {eq.warning_times_slow[ind]}
warning time w/ half duration: {eq.warning_times_s_dur[ind]}
half duration: {eq.half_dur}
''')
plt.figure()
plt.plot(castle_2.mmi, castle_2.warning_times_s, alpha=0.3, c='k')
plt.plot(castle_2.mmi, castle_2.warning_times_s_dur, alpha=0.3, c='r')
plt.savefig('Figures/misc/castle rupdur test.png')
