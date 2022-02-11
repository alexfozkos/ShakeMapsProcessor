import numpy as np
import UsefulFunctions as uf
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 16})

anc_05 = uf.Earthquake('Data/AncScenarioGrids/grid05.xml')
anc_10 = uf.Earthquake('Data/AncScenarioGrids/grid10.xml')
anc_20 = uf.Earthquake('Data/AncScenarioGrids/grid20.xml')
anc_30 = uf.Earthquake('Data/AncScenarioGrids/grid30.xml')
anc_40 = uf.Earthquake('Data/AncScenarioGrids/grid40.xml')
anc_50 = uf.Earthquake('Data/AncScenarioGrids/grid50.xml')
anc_75 = uf.Earthquake('Data/AncScenarioGrids/grid75.xml')
anc_100 = uf.Earthquake('Data/AncScenarioGrids/grid100.xml')
anc_125 = uf.Earthquake('Data/AncScenarioGrids/grid125.xml')
anc_150 = uf.Earthquake('Data/AncScenarioGrids/grid150.xml')

# anc_real = uf.Earthquake('Data/AncScenarioGrids/gridreal.xml')
# anc_467 = uf.Earthquake('Data/AncScenarioGrids/grid467.xml')
# den_05 = uf.Earthquake('Data/griddenali.xml')


def pgaVsDistComparison(eqlist, names, title='Default Name', xlabel='Epicentral Distance (km)',
                        ylabel='PGA (%g)', xmin= 0, xmax=500, scale='linear', figsize=None, n=1, ymin=0):
    # I'm sick of typing 10+ lines for every plot! Time to make the standard code block its own function...
    # Takes a list of earthquakes, a list of names for those earthquakes (in same order), then different pyplot
    # parameters. Will auto configure figsize if left alone. Will handle ymin for log scales. Auto configures ymax

    # Global font size
    plt.rcParams['font.size'] = '16'
    # create fig w/ subplots, can do more than 2 if define parameter as a list of eq's then loop through them instead
    if figsize is None:
        figsize = (12, (len(eqlist) + 1) * 4)

    # colors is a list of colors that will scycle through each time a plot is plotted
    colors = ['blue', 'darkorange', 'red', 'green', 'purple', 'cyan', 'magenta']

    # set ymin to 0.0001 if using log scale (log cant be 0)
    if scale == 'log':
        ymin = 0.0001

    # Auto configure ymax (rounds up to nearest 10)
    pgamax = 0
    for eq in eqlist:
        if np.max(eq.pga) > pgamax:
            pgamax = np.max(eq.pga)

    #  create figure and loop through each earthquake to plot for each individually
    fig, ax = plt.subplots(len(eqlist) + 1, figsize=figsize)
    fig.suptitle(title, fontsize=24)
    for i in range(0, len(eqlist)):
        color = colors[i % len(colors)]
        ax[i].set_yscale(scale)
        ax[i].scatter(eqlist[i].warning_times_s[::n], eqlist[i].pga[::n], s=0.1, c=color)
        ax[i].set_title(names[i], fontsize=20)
        ax[i].set_xlabel(xlabel)
        ax[i].set_ylabel(ylabel)
        ax[i].set_xlim(xmin, xmax)
        ax[i].set_ylim(ymin, np.ceil(pgamax / 10) * 10)

    # plot them overlayed
    ax[-1].set_yscale(scale)
    for i in range(0, len(eqlist)):
        color = colors[i % len(colors)]
        ax[-1].scatter(eqlist[i].warning_times_s[::n], eqlist[i].pga[::n], s=0.1, c=color, label=names[i])
    t = 'Plots overlayed'
    ax[-1].set_title(t)
    ax[-1].set_xlabel(xlabel)
    ax[-1].set_ylabel(ylabel)
    ax[-1].set_xlim(xmin, xmax)
    ax[-1].set_ylim(ymin, np.ceil(pgamax / 10) * 10)

    plt.legend(markerscale=15, scatterpoints=1, loc=1)
    fig.tight_layout()

    plt.savefig('Figures/AncScenario/' + title + '.png')


eqlist = [anc_05, anc_10, anc_20,anc_30,anc_40,anc_50,anc_75,anc_100,anc_125,anc_150]
pgaVsDistComparison(eqlist, ['5 km', '10 km','20 km','30 km','40 km','50 km','75 km','100 km','125 km','150 km'],
                    title='5 km to 150 km scenarios PGAvWT', xmin=-10, xmax=60, xlabel='Warning Time (s)')

# fig, ax = plt.subplots(len(eqlist), figsize=(8,10))
# for i in range(len(eqlist)):
#     eq = eqlist[i]
#     ax[i].scatter(eq.pga, eq.mmi, s=0.6)
#     ax[i].set_xlabel('PGA')
#     ax[i].set_xscale('log')
#     ax[i].set_ylabel('MMI')
#     ax[i].axvline(6.2)
#     ax[i].axhline(4.5, c='r', ls='dashed')
#     ax[i].set_xlim(2, 7)
#     ax[i].set_ylim(2.5, 5)
#     ax[i].set_title(eq.event['event_id'])
# plt.tight_layout()
# plt.show()


# #  Auto selection comparison
# pgaVsDistComparison([anc_05, anc_05_auto], ['Manual GMPEs', 'Auto-selected GMPEs'],
#                     title='Manual vs Automatic GMPE selection at 5 km', xlim=200, scale='linear')
# #  Real vs 5 km auto
# pgaVsDistComparison([anc_real, anc_05_auto], ['Real Earthquake', '5 km Auto'],
#                     title='Real Quake (46.7 km) vs 5 km Auto GMPE', xlim=200, scale='linear')
# #  Real vs 5 km auto vs 5 km manual
# pgaVsDistComparison([anc_real, anc_05_auto, anc_05], ['Real Earthquake', '5 km Auto', '5 km Manual'],
#                     title='Real Quake vs Auto and Manual GMPE selection at 5 km', xlim=200, scale='linear')

plt.rcParams['font.size'] = '16'
# Wave Arrivals
# t = np.linspace(0, 120, 120)
# figure, ax = plt.subplots(2, figsize=(12, 12))
# ax[0].grid(c='gray', ls='dashed', lw=1)
# ax[0].scatter(anc_real.distances_epi, anc_real.arrivals_p, s=1,  c='blue', label='P wave arrivals')
# ax[0].scatter(anc_real.distances_epi, anc_real.arrivals_s, s=1, c='orange', label='S wave arrivals')
# ax[0].scatter(anc_real.station_distances, np.zeros(anc_real.station_distances.shape), s=20, c='red', marker='^')
# ax[0].set_ylabel('Arrival Time (s)')
# ax[0].set_xlabel('Epicentral Distance (km)')
# ax[0].set_title('P vs S Wave Arrival Times')
# ax[0].axhline(anc_real.detection_time, c='k', ls='dotted')
# ax[0].axvline(46.06, c='k', ls='dotted')
# ax[0].set_ylim(-1, 60)
# ax[0].set_xlim(0, 200)
# ax[0].axhline(y=0, color='k')
# ax[0].axvline(x=0, color='k')
# ax[0].legend(loc='lower right', markerscale=20)
# # Warning time
#
# ax[1].grid(c='gray', ls='dashed', lw=1)
# ax[1].scatter(anc_real.station_distances, np.zeros(anc_real.station_distances.shape), s=20, c='red', marker='^')
# ax[1].scatter(anc_real.distances_epi, anc_real.warning_times_s, s=1, c='green', label='Warning Time')
# ax[1].axhline(y=0, color='k')
# ax[1].axvline(x=0, color='k')
# ax[1].set_ylim(-5, 60)
# ax[1].set_xlim(0, 200)
# ax[1].set_ylabel('Warning Time (s)')
# ax[1].set_xlabel('Epicentral Distance (km)')
# ax[1].set_title('Distance Vs Warning Time')
# ax[1].text(25, 53, 'Time to create and send out a warning: {} s'.format(round(anc_real.time_to_warning, 1)))
# pga_plot = ax[1].twinx()
# pga_plot.scatter(anc_real.distances_epi, anc_real.pga, s=1, c=anc_real.pga, cmap='plasma', label='Shaking (PGA %g)')
# pga_plot.set_ylabel('Shaking (PGA %g)')

# plt.tight_layout()
# plt.show()

# region Shaking vs distance and warning time comparison plots
# figure, ax = plt.subplots(2, figsize=(12, 12))
# ax[0].grid(c='gray', ls='dashed', lw=1)
# z1 = ax[0].scatter(anc_real.distances_epi, anc_real.pgv, s=2,  c=anc_real.pgv, cmap='turbo', label='Shaking (PGV)')
# ax[0].set_ylabel('PGV (m/s)')
# ax[0].set_xlabel('Epicentral Distance (km)')
# ax[0].set_title('Shaking vs Epicentral Distance')
# ax[0].set_ylim(-1, 50)
# ax[0].set_xlim(0, 200)
# ax[0].axhline(y=0, color='k')
# ax[0].axvline(x=0, color='k')
#
# ax[1].grid(c='gray', ls='dashed', lw=1)
# ax[1].scatter(anc_real.warning_times_s, anc_real.pgv, s=2,  c=anc_real.pgv, cmap='turbo', label='Shaking (PGV)')
# ax[1].set_ylabel('PGV (m/s)')
# ax[1].set_xlabel('Warning Time (s)')
# ax[1].set_title('Shaking vs Warning Time')
# ax[1].set_ylim(-1, 50)
# ax[1].set_xlim(-5, 35)
# ax[1].axhline(y=0, color='k')
# ax[1].axvline(x=0, color='k')
# ax[1].axvline(x=5, color='darkgray', lw=2, ls='dotted')
# # ax[1].legend(loc='upper right', markerscale=20)
#
# plt.tight_layout()
# plt.show()
# endregion



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Here Be Dragons ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

# n = 1
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

# n = 25
#
# fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 12))
# fig.suptitle('PGA vs Distance for Real Quake vs 46.7 km Scenario')
# ax1.set_yscale('log')
# ax1.scatter(anc_real.distances_epi[::n], anc_real.pga[::n], s=0.1, c='blue')
# ax1.set_title('Real Earthquake')
# ax1.set_xlabel('Epicentral Distance (km)')
# ax1.set_ylabel('PGA (%g)')
# ax1.set_xlim(0, 1000)
# ax1.set_ylim(0.0001, 50)
#
# ax2.set_title('46.7 km Scenario')
# ax2.set_yscale('log')
# ax2.scatter(anc_467.distances_epi[::n], anc_467.pga[::n], s=0.1, c='orange')
# ax2.set_xlim(0, 1000)
# ax2.set_ylim(0.0001, 50)
# ax2.set_xlabel('Epicentral Distance (km)')
# ax2.set_ylabel('PGA (%g)')
#
# fig.tight_layout()
# plt.savefig('Figures/AncScenario/PGA vs Dist for Real and 46.7 km Scenario.png')
#
# plt.clf()
#
#
# fig, ax1 = plt.subplots(figsize=(12, 12))
# fig.suptitle('Real Quake vs 46.7 km Scenario Overlayed')
# ax1.set_yscale('log')
# ax1.scatter(anc_real.distances_epi[::n], anc_real.pga[::n], s=0.1, c='blue', label='Real Earthquake')
# ax1.scatter(anc_467.distances_epi[::n], anc_467.pga[::n], s=0.1, c='orange', label='46.7 km Scenario')
# ax1.set_xlabel('Epicentral Distance (km)')
# ax1.set_ylabel('PGA (%g)')
# # ax1.set_xlim(0, 1000)
# ax1.set_ylim(0.0001, 50)
# plt.legend(markerscale=15, scatterpoints=1)
# fig.tight_layout()
# plt.savefig('Figures/AncScenario/Real Quake vs 46.7 km Scenario Overlayed.png')
#
# plt.clf()

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
