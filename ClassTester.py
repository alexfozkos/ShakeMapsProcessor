import numpy as np
import UsefulFunctions as uf
from matplotlib import pyplot as plt

# eq = uf.Earthquake()


# Download xmls and create multiple Earthquake objects from url list
urls = ['https://earthquake.alaska.edu/sites/all/web/shakemap/ak0219neiszm/grid.xml',  # Chignik Earthquake
        'https://earthquake.alaska.edu/sites/all/web/shakemap/ak021bt4ffvw/grid.xml',  # 4.9 Pump Station
        'https://earthquake.alaska.edu/sites/all/web/shakemap/ak0216xu2rod/grid.xml'  # 6.1 by Fairbanks
        ]

events = []
for i in urls:
    uf.download(i)
    events.append(uf.Earthquake())

# assign objects some names and add random noise -0.05 to 0.05 to mmi
rng = np.random.default_rng()
eq_Chignik = events[0]
noise = 0.1 * rng.random(eq_Chignik.mmi.shape) - 0.05
Chignik_noisy_mmi = eq_Chignik.mmi + noise

eq_Pump = events[1]
noise = 0.1 * rng.random(eq_Pump.mmi.shape) - 0.05
Pump_noisy_mmi = eq_Pump.mmi + noise

eq = events[2]
noise = 0.1 * rng.random(eq.mmi.shape) - 0.05
eq_noisy_mmi = eq.mmi + noise


# # Plots for Distance V Warning Times and S arrivals V MMI
# fig, (ax1, ax2) = plt.subplots(2, figsize=(16, 16))
#
# ax1.plot(eq.distances, eq.warning_times)
# ax1.set(xlabel='distance (m)', ylabel='warning time (s)')
#
# ax2.scatter(eq.arrivals_s, eq.mmi, s=0.5)
# ax2.set(xlabel='S arrival time (s)', ylabel='MMI')
#
# fig.tight_layout()
# plt.savefig('tester.png')

# plt.clf()


# # Plot warning times V distance with colorbars for MMI and PGA(%g)
# # rng = np.random.default_rng()
# # noise = 10 * rng.random(eq.warning_times.shape) - 5
#
# n = 1
#
# fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 12))
# fig.suptitle('Warning Times Vs Epicentral Distance')
# z1 = ax1.scatter(eq.distances[::n], eq.warning_times[::n], s=0.1, c=eq.mmi[::n], marker=',', cmap='rainbow')
# ax1.set_xlabel('Epicentral Distance (km)')
# ax1.set_ylabel('Warning Time (s)')
# plt.colorbar(z1, label='MMI', ax=ax1)
#
# z2 = ax2.scatter(eq.distances[::n], eq.warning_times[::n], s=0.1, c=eq.pga[::n], marker=',', cmap='rainbow')
# ax2.set_xlabel('Epicentral Distance (km)')
# ax2.set_ylabel('Warning Time (s)')
# plt.colorbar(z2, label='PGA (%g)', ax=ax2)
#
# fig.tight_layout()
# plt.savefig('Warning Times vs Epicentral Distance')


# Warning Times vs MMI triple plot

n = 25  # plot every nth point
fig, ax1 = plt.subplots(figsize=(16, 12))

ax1.title.set_text('S arrival warning times versus MMI for 3 separate events (every {} points)'.format(n))
ax1.set_xlabel('Maximum warning time before S-wave arrival (s)')
ax1.set_ylabel('MMI')
ax1.scatter(x=eq.warning_times[::n] + rng.random(eq.warning_times.shape)[::n] - 0.5, y=eq_noisy_mmi[::n], c='green', marker='o', s=0.8, label='6.1 near Fairbanks')
ax1.scatter(x=eq_Pump.warning_times[::n] + rng.random(eq_Pump.warning_times.shape)[::n] - 0.5, y=Pump_noisy_mmi[::n], c='blue', marker='^', s=0.8, label='4.9 near Pump Station')
ax1.scatter(x=eq_Chignik.warning_times[::n] + rng.random(eq_Chignik.warning_times.shape)[::n] - 0.5, y=Chignik_noisy_mmi[::n], c='red', marker='D', s=0.8, label='7.8 Chignik Earthquake')
ax1.set_xlim(0, 300)

ax1.axvline(x=5, color='black', linestyle='dashed', label='5 Second Warning Time Threshold')
ax1.axvline(x=10, color='black', linestyle='dotted', label='10 Second Warning Time Threshold')

plt.legend()
plt.savefig('Warning times vs MMI for 3 earthquakes')
