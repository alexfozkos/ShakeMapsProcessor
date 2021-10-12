import numpy as np
import UsefulFunctions as uf
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 28})

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


# Plots for Distance V Warning Times and S arrivals V MMI
fig, (ax1, ax2) = plt.subplots(2, figsize=(16, 16))

ax1.plot(eq.distances, eq.warning_times)
ax1.set(xlabel='epicentral distance (km)', ylabel='warning time (s)')
ax1.axhline(y=0, ls='--', c='black')

ax2.scatter(eq.warning_times, eq.mmi, s=0.5)
ax2.set(xlabel='warning time (s)', ylabel='MMI')
ax2.axvline(x=0, ls='--', c='black')

fig.tight_layout()
plt.savefig('Figures/WTvsDist and MMIvsWT.png')

plt.clf()


# Plot warning times V distance with colorbars for MMI and PGA(%g)
# rng = np.random.default_rng()
# noise = 10 * rng.random(eq.warning_times.shape) - 5

n = 1

fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 12))
fig.suptitle('Warning Times Vs Epicentral Distance')
z1 = ax1.scatter(eq.distances[::n], eq.warning_times[::n], s=0.1, c=eq.mmi[::n], marker=',', cmap='rainbow')
ax1.set_xlabel('Epicentral Distance (km)')
ax1.set_ylabel('Warning Time (s)')
ax1.axhline(y=0, ls='--', c='black')
plt.colorbar(z1, label='MMI', ax=ax1)

z2 = ax2.scatter(eq.distances[::n], eq.warning_times[::n], s=0.1, c=eq.pga[::n], marker=',', cmap='rainbow')
ax2.set_xlabel('Epicentral Distance (km)')
ax2.set_ylabel('Warning Time (s)')
ax2.axhline(y=0, ls='--', c='black')
plt.colorbar(z2, label='PGA (%g)', ax=ax2)

fig.tight_layout()
plt.savefig('Figures/Warning Times vs Epicentral Distance.png')

plt.clf()

# Warning Times vs MMI triple plot
plt.rcParams.update({'font.size': 15})
# might be worth it to decimate the data randomly rather than in order?
n = 50  # plot every nth point
fig, ax1 = plt.subplots(figsize=(16, 12))

ax1.title.set_text('MMI vs Warning Time for 3 earthquakes (every {} data points)'.format(n))
ax1.set_xlabel('Maximum warning time before S-wave arrival (s)')
ax1.set_ylabel('MMI')
ax1.scatter(x=eq.warning_times[::n] + rng.random(eq.warning_times.shape)[::n] - 0.5, y=eq_noisy_mmi[::n], c='green', s=0.8, label='6.1 near Fairbanks')
ax1.scatter(x=eq_Pump.warning_times[::n] + rng.random(eq_Pump.warning_times.shape)[::n] - 0.5, y=Pump_noisy_mmi[::n], c='blue', s=0.8, label='4.9 near Pump Station')
ax1.scatter(x=eq_Chignik.warning_times[::n] + rng.random(eq_Chignik.warning_times.shape)[::n] - 0.5, y=Chignik_noisy_mmi[::n], c='red', s=0.8, label='7.8 Chignik Earthquake')
# ax1.set_xlim(-uf.Earthquake.ttp, 60-uf.Earthquake.ttp)

ax1.axvline(x=0, color='black', lw=3, c='maroon', label='0 Second Warning Time Threshold')
ax1.axvline(x=5, color='black', lw=3, ls='dashed', label='5 Second Warning Time Threshold')
ax1.axvline(x=10, color='black', lw=3, ls='dotted', label='10 Second Warning Time Threshold')

plt.legend()
# plt.legend(loc=3)
plt.savefig('Figures/MMI vs Warning Time for 3 earthquakes.png')
