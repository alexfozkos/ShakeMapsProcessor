import numpy as np
import UsefulFunctions as uf
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 28})

# anc_05 = uf.Earthquake('Data/AncScenarioGrids/grid05.xml')
# anc_10 = uf.Earthquake('Data/AncScenarioGrids/grid10.xml')
# anc_20 = uf.Earthquake('Data/AncScenarioGrids/grid20.xml')
# anc_30 = uf.Earthquake('Data/AncScenarioGrids/grid30.xml')
# anc_40 = uf.Earthquake('Data/AncScenarioGrids/grid40.xml')
# anc_50 = uf.Earthquake('Data/AncScenarioGrids/grid50.xml')
anc_real = uf.Earthquake('Data/AncScenarioGrids/gridreal.xml')
anc_467 = uf.Earthquake('Data/AncScenarioGrids/grid467.xml')
# print('mins')
# print(np.min(anc_05.pga),np.min(anc_10.pga),np.min(anc_20.pga),np.min(anc_30.pga),np.min(anc_40.pga),np.min(anc_50.pga))
# print('maxs')
# print(np.max(anc_05.pga),np.max(anc_10.pga),np.max(anc_20.pga),np.max(anc_30.pga),np.max(anc_40.pga),np.max(anc_50.pga))

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
#
# fig, ax = plt.subplots(2, 3, figsize=(20,20))
# for i in ax:
#     for j in i:
#         j.set_xlim(0, 1000)
#         j.set_ylim(0.001, 100)
#         j.set_yscale('log')
#
# fig.suptitle('PGA vs Distance for 5 km to 50 km')
# # 5km
# ax[0, 0].scatter(anc_05.distances_epi[::n], anc_05.pga[::n], s=0.1)
# ax[0, 0].set_xlabel('Epicentral Distance (km)')
# ax[0, 0].set_ylabel('PGA (%g)')
# ax[0, 0].set_title('05 km Scenario')
# # ax[0].set_xlim(0, 1000)
# # ax[0].set_ylim(0.0001, 70)
#
# # 10km
# ax[0, 1].scatter(anc_10.distances_epi[::n], anc_10.pga[::n], s=0.1)
# ax[0, 1].set_xlabel('Epicentral Distance (km)')
# ax[0, 1].set_ylabel('PGA (%g)')
# ax[0, 1].set_title('10 km Scenario')
# # ax[1].set_xlim(0, 1000)
# # ax[1].set_ylim(0.0001, 70)
# plt.yscale('log')
#
# # 20km
# ax[0, 2].scatter(anc_20.distances_epi[::n], anc_20.pga[::n], s=0.1)
# ax[0, 2].set_xlabel('Epicentral Distance (km)')
# ax[0, 2].set_ylabel('PGA (%g)')
# ax[0, 2].set_title('20 km Scenario')
# # ax[2].set_xlim(0, 1000)
# # ax[2].set_ylim(0.0001, 70)
# plt.yscale('log')
#
# # 30km
# ax[1, 0].scatter(anc_30.distances_epi[::n], anc_30.pga[::n], s=0.1)
# ax[1, 0].set_xlabel('Epicentral Distance (km)')
# ax[1, 0].set_ylabel('PGA (%g)')
# ax[1, 0].set_title('30 km Scenario')
# # ax[3].set_xlim(0, 1000)
# # ax[3].set_ylim(0.0001, 70)
# plt.yscale('log')
#
# # 40km
# ax[1, 1].scatter(anc_40.distances_epi[::n], anc_40.pga[::n], s=0.1)
# ax[1, 1].set_xlabel('Epicentral Distance (km)')
# ax[1, 1].set_ylabel('PGA (%g)')
# ax[1, 1].set_title('40 km Scenario')
# # ax[4].set_xlim(0, 1000)
# # ax[4].set_ylim(0.0001, 70)
# plt.yscale('log')
#
# # 50km
# ax[1, 2].scatter(anc_50.distances_epi[::n], anc_50.pga[::n], s=0.1)
# ax[1, 2].set_xlabel('Epicentral Distance (km)')
# ax[1, 2].set_ylabel('PGA (%g)')
# ax[1, 2].set_title('50 km Scenario')
# # ax[5].set_xlim(0, 1000)
# # ax[5].set_ylim(0.0001, 70)
#
# fig.tight_layout()
# plt.savefig('Figures/AncScenario/PGA vs Dist for top 50 km (log).png')
#
# plt.clf()

n = 25

fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 12))
fig.suptitle('PGA vs Distance for Real Quake vs 46.7 km Scenario')
ax1.set_yscale('log')
ax1.scatter(anc_real.distances_epi[::n], anc_real.pga[::n], s=0.1, c='blue')
ax1.set_title('Real Earthquake')
ax1.set_xlabel('Epicentral Distance (km)')
ax1.set_ylabel('PGA (%g)')
ax1.set_xlim(0, 1000)
ax1.set_ylim(0.0001, 50)

ax2.set_title('46.7 km Scenario')
ax2.set_yscale('log')
ax2.scatter(anc_467.distances_epi[::n], anc_467.pga[::n], s=0.1, c='orange')
ax2.set_xlim(0, 1000)
ax2.set_ylim(0.0001, 50)
ax2.set_xlabel('Epicentral Distance (km)')
ax2.set_ylabel('PGA (%g)')

fig.tight_layout()
plt.savefig('Figures/AncScenario/PGA vs Dist for Real and 46.7 km Scenario.png')

plt.clf()


fig, ax1 = plt.subplots(figsize=(12, 12))
fig.suptitle('Real Quake vs 46.7 km Scenario Overlayed')
ax1.set_yscale('log')
ax1.scatter(anc_real.distances_epi[::n], anc_real.pga[::n], s=0.1, c='blue', label='Real Earthquake')
ax1.scatter(anc_467.distances_epi[::n], anc_467.pga[::n], s=0.1, c='orange', label='46.7 km Scenario')
ax1.set_xlabel('Epicentral Distance (km)')
ax1.set_ylabel('PGA (%g)')
# ax1.set_xlim(0, 1000)
ax1.set_ylim(0.0001, 50)
plt.legend(markerscale=15, scatterpoints=1)
fig.tight_layout()
plt.savefig('Figures/AncScenario/Real Quake vs 46.7 km Scenario Overlayed.png')

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
