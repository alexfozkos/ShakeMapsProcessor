import numpy as np
import UsefulFunctions as uf
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 28})

anc_05 = uf.Earthquake('Data/AncScenarioGrids/grid05.xml')
anc_real = uf.Earthquake('Data/AncScenarioGrids/gridreal.xml')


# Plots for Distance V Warning Times and S arrivals V MMI
# fig, (ax1, ax2) = plt.subplots(2, figsize=(16, 16))
#
# ax1.plot(anc_real.distances_epi, anc_real.warning_times_s)
# ax1.set(xlabel='epicentral distance (km)', ylabel='warning time (s)')
# ax1.axhline(y=0, ls='--', c='black')
#
# ax2.scatter(anc_real.warning_times_s, anc_real.mmi, s=0.5)
# ax2.set(xlabel='warning time (s)', ylabel='MMI')
# ax2.axvline(x=0, ls='--', c='black')
#
# fig.tight_layout()
# plt.savefig('Figures/AncScenario/5 km WTvsDist and MMIvsWT.png')
#
# plt.clf()


# Plot warning times V distance with colorbars for MMI and PGA(%g)
# rng = np.random.default_rng()
# noise = 10 * rng.random(eq.warning_times.shape) - 5

n = 1

fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 12))
fig.suptitle('PGA vs Epicentral Distance for Real and 05')
z1 = ax1.scatter(anc_real.distances_epi[::n], anc_real.pga[::n], s=0.1, c='blue')
ax1.set_xlabel('Epicentral Distance (km)')
ax1.set_ylabel('PGA (%g)')
ax1.set_title('Real Earthquake')
ax1.set_xlim(0, 500)
ax1.set_ylim(0, 70)

z2 = ax2.scatter(anc_05.distances_epi[::n], anc_05.pga[::n], s=0.1, c='orange')
ax2.set_xlabel('Epicentral Distance (km)')
ax2.set_ylabel('PGA (%g)')
ax2.set_title('5 km Scenario')
ax2.set_xlim(0, 500)
ax2.set_ylim(0, 70)


fig.tight_layout()
plt.savefig('Figures/AncScenario/PGA vs Dist for Real and 05.png')

plt.clf()

fig, ax1 = plt.subplots(figsize=(12, 12))
fig.suptitle('PGA vs Epicentral Distance for Real and 05 combined')
ax1.scatter(anc_real.distances_epi[::n], anc_real.pga[::n], s=0.1, c='blue')
ax1.set_xlabel('Epicentral Distance (km)')
ax1.set_ylabel('PGA (%g)')
ax1.scatter(anc_05.distances_epi[::n], anc_05.pga[::n], s=0.1, c='orange')
ax1.set_xlim(0, 500)
ax1.set_ylim(0, 70)

fig.tight_layout()
plt.savefig('Figures/AncScenario/PGA vs Dist for Real and 05 combined.png')

plt.clf()

# # Warning Times vs MMI triple plot
# plt.rcParams.update({'font.size': 15})
# # might be worth it to decimate the data randomly rather than in order?
# n = 50  # plot every nth point
# fig, ax1 = plt.subplots(figsize=(16, 12))
#
# ax1.title.set_text('MMI vs Warning Time for 3 earthquakes (every {} data points)'.format(n))
# ax1.set_xlabel('Maximum warning time before S-wave arrival (s)')
# ax1.set_ylabel('MMI')
# ax1.scatter(x=eq.warning_times[::n] + rng.random(eq.warning_times.shape)[::n] - 0.5, y=eq_noisy_mmi[::n], c='green', s=0.8, label='6.1 near Fairbanks')
# ax1.scatter(x=eq_Pump.warning_times[::n] + rng.random(eq_Pump.warning_times.shape)[::n] - 0.5, y=Pump_noisy_mmi[::n], c='blue', s=0.8, label='4.9 near Pump Station')
# ax1.scatter(x=eq_Chignik.warning_times[::n] + rng.random(eq_Chignik.warning_times.shape)[::n] - 0.5, y=Chignik_noisy_mmi[::n], c='red', s=0.8, label='7.8 Chignik Earthquake')
# # ax1.set_xlim(-uf.Earthquake.ttp, 60-uf.Earthquake.ttp)
#
# ax1.axvline(x=0, color='black', lw=3, c='maroon', label='0 Second Warning Time Threshold')
# ax1.axvline(x=5, color='black', lw=3, ls='dashed', label='5 Second Warning Time Threshold')
# ax1.axvline(x=10, color='black', lw=3, ls='dotted', label='10 Second Warning Time Threshold')
#
# plt.legend()
# # plt.legend(loc=3)
# plt.savefig('Figures/MMI vs Warning Time for 3 earthquakes.png')
