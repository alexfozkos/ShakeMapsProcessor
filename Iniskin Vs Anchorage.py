import numpy as np
import UsefulFunctions as uf
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 28})

Anchorage = uf.Earthquake('Data/Anchorage_grid.xml')
Iniskin = uf.Earthquake('Data/Iniskin_grid.xml')

rng = np.random.default_rng()

noise = 0.1 * rng.random(Anchorage.mmi.shape) - 0.05
Anchorage_noisy_mmi = Anchorage.mmi + noise

noise = 0.1 * rng.random(Iniskin.mmi.shape) - 0.05
Iniskin_noisy_mmi = Iniskin.mmi + noise

# Warning Time Vs Distance plots
n = 1

fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 12))
fig.suptitle('Warning Times Vs Hypocentral Distance')
z1 = ax1.scatter(Anchorage.distances_hypo[::n], Anchorage.warning_times_s[::n], s=0.1, c=Anchorage.mmi[::n], marker=',', cmap='rainbow')
ax1.set_xlabel('Hypocentral Distance (km)')
ax1.set_ylabel('Warning Time (s)')
ax1.title.set_text('Anchorage')
ax1.axhline(y=0, ls='--', c='black')
plt.colorbar(z1, label='MMI', ax=ax1)

z2 = ax2.scatter(Iniskin.distances_hypo[::n], Iniskin.warning_times_s[::n], s=0.1, c=Iniskin.mmi[::n], marker=',', cmap='rainbow')
ax2.set_xlabel('Hypocentral Distance (km)')
ax2.set_ylabel('Warning Time (s)')
ax2.title.set_text('Iniskin')
ax2.axhline(y=0, ls='--', c='black')
plt.colorbar(z2, label='MMI', ax=ax2)

fig.tight_layout()
plt.savefig('Figures/Iniskin Vs Anchorage/Iniskin Vs Anchorage WT-Dist.png')

plt.clf()

# Warning Times vs MMI Double plot
plt.rcParams.update({'font.size': 15})
# might be worth it to decimate the data randomly rather than in order?
n = 5  # plot every nth point
fig, ax1 = plt.subplots(figsize=(16, 12))

ax1.title.set_text('MMI vs Warning Time, Anchorage and Iniskin (every {} data points)'.format(n))
ax1.set_xlabel('Warning Time (s)')
ax1.set_ylabel('MMI')
ax1.scatter(x=Anchorage.warning_times_s[::n], y=Anchorage_noisy_mmi[::n], c='red', s=0.8, label='Anchorage')
ax1.scatter(x=Iniskin.warning_times_s[::n], y=Iniskin_noisy_mmi[::n], c='blue', s=0.8, label='Iniskin')
# ax1.set_xlim(-uf.Earthquake.ttp, 60-uf.Earthquake.ttp)

ax1.axvline(x=0, color='black', lw=3, c='maroon', label='0 Second Warning Time Threshold')
ax1.axvline(x=5, color='black', lw=3, ls='dashed', label='5 Second Warning Time Threshold')
ax1.axvline(x=10, color='black', lw=3, ls='dotted', label='10 Second Warning Time Threshold')

plt.legend()
# plt.legend(loc=3)
plt.savefig('Figures/Iniskin Vs Anchorage/Iniskin Vs Anchorage MMI-WT')


