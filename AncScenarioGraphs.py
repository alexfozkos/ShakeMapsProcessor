import math
import numpy as np
import UsefulFunctions as uf
import matplotlib

matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 16})

anc_05 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid05.xml')
# anc_10 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid10.xml')
# anc_20 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid20.xml')
# anc_25 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid25.xml')
# anc_30 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid30.xml')
# anc_40 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid40.xml')
anc_50 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid50.xml')
# anc_75 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid75.xml')
# anc_100 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid100.xml')
# anc_125 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid125.xml')
anc_150 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid150.xml')
# anc_175 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid175.xml')
# anc_200 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid200.xml')

anc_true = uf.Earthquake('Data/AncScenarioGrids/gridtrue.xml')
# anc_real = uf.Earthquake('Data/AncScenarioGrids/gridreal.xml')
# anc_467 = uf.Earthquake('Data/AncScenarioGrids/grid467.xml')
# den_05 = uf.Earthquake('Data/griddenali.xml')


def pgaVsDistComparison(eqlist, names, title='Default Name', xlabel='Epicentral Distance (km)',
                        ylabel='PGA (%g)', xmin=0, xmax=500, scale='linear', figsize=None, n=1, ymin=0, ncols=2, size=1,
                        colors=None):
    # I'm sick of typing 10+ lines for every plot! Time to make the standard code block its own function...
    # Takes a list of earthquakes, a list of names for those earthquakes (in same order), then different pyplot
    # parameters. Will auto configure figsize if left alone. Will handle ymin for log scales. Auto configures ymax

    # Global font size
    plt.rcParams['font.size'] = '16'
    # create fig w/ subplots, can do more than 2 if define parameter as a list of eq's then loop through them instead
    if figsize is None:
        figsize = (16, (len(eqlist) + 1) * 4)

    # colors is a list of colors that will scycle through each time a plot is plotted
    if colors is None:
        colors = ['blue', 'darkorange', 'red', 'green', 'purple', 'cyan', 'magenta']

    # set ymin to 0.0001 if using log scale (log cant be 0)
    if scale == 'log':
        ymin = 0.1
        ymax = 100

    # Auto configure ymax (rounds up to nearest 10)
    pgamax = 0
    for eq in eqlist:
        if np.max(eq.pga) > pgamax:
            pgamax = np.max(eq.pga)

    #  create figure and loop through each earthquake to plot for each individually
    nrows = math.ceil((len(eqlist) + 1) / ncols)
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    fig.suptitle(title, fontsize=24)

    previous_max = pgamax
    k = 0
    for i in range(nrows):
        for j in range(ncols):
            if not k == len(eqlist):
                color = colors[k % len(colors)]
                ax[i, j].set_yscale(scale)
                ax[i, j].scatter(eqlist[i].distances_epi[::n], eqlist[k].pga[::n], s=size, c=color)
                # ax[i, j].axhline(previous_max, c='k', ls='--', lw=3)
                ax[i, j].set_title(names[k], fontsize=20)
                ax[i, j].set_xlabel(xlabel)
                ax[i, j].set_ylabel(ylabel)
                ax[i, j].set_xlim(xmin, xmax)
                # ax[i, j].set_ylim(ymin, np.ceil(pgamax / 10) * 10)
                ax[i, j].set_ylim(ymin, ymax)
                previous_max = eqlist[k].pga.max()
                k += 1

    # plot them overlayed
    ax[-1, -1].set_yscale(scale)
    for i in range(0, len(eqlist)):
        color = colors[i % len(colors)]
        ax[-1, -1].scatter(eqlist[i].distances_epi[::n], eqlist[i].pga[::n], s=size, c=color, label=names[i], alpha=0.3)
    t = 'Plots overlayed'
    ax[-1, -1].set_title(t)
    ax[-1, -1].set_xlabel(xlabel)
    ax[-1, -1].set_ylabel(ylabel)
    ax[-1, -1].set_xlim(xmin, xmax)
    # ax[-1, -1].set_ylim(ymin, np.ceil(pgamax / 10) * 10)
    ax[-1, -1].set_ylim(ymin, ymax)
    plt.legend(markerscale=15, scatterpoints=1, loc=1)
    fig.tight_layout(rect=[0, 0, 1, 0.98])

    plt.savefig('Figures/AncScenario/' + title + '.png')


eqlist_mini = [anc_05, anc_50, anc_150]
eqlabels_mini = ['5 km', '50 km', '150 km']
# eqlist = [anc_05, anc_25, anc_50, anc_75, anc_100, anc_125, anc_150]
# depths = [5, 25, 50, 75, 100, 125, 150]
# eqlist_long = [anc_05, anc_10, anc_20, anc_30, anc_40, anc_50, anc_75, anc_100, anc_125, anc_150, anc_175, anc_200]
# eqlabels_long = ['5 km', '10 km', '20 km', '30 km', '40 km', '50 km', '75 km', '100 km', '125 km', '150 km', '175 km', '200 km']
# pgaVsDistComparison(eqlist_mini, eqlabels_mini, title='5, 50, and 150 km scenarios PGAvDist', xmax=500, scale='log',
#                     colors=['r','g','b'])


# colors = ['r', 'g', 'b']
plt.figure(figsize=(8, 6))
plt.scatter(anc_true.mmi, anc_true.warning_times_s, c='rebeccapurple', s=10)
plt.xlabel('MMI')
plt.ylabel('Warning Time (s)')
plt.axhline(0, c='k')
plt.xlim(2.5, 8)
# plt.xscale('log')
plt.ylim(bottom=-15, top=120)
plt.title('Anchorage 2018: Warning Time vs MMI')
# plt.tight_layout(rect=(0, 0, 1, 0.99))
plt.savefig('Figures/AncScenario/Anchorage 2018 WT vs MMI.png', dpi=400)
plt.show()

# fig, ax = plt.subplots(figsize=(12, 12))
# fig.suptitle('PGA vs Distance for 3 Different Source Depths')
# for i in range(len(eqlist_mini)):
#     eq = eqlist_mini[i]
#     ax.scatter(eq.distances_epi, eq.pga, c=colors[i], s=2, label=eqlabels_mini[i])
# ax.axhline(0, c='k', lw=1)
# # ax.set_xscale('log')
# # ax.invert_xaxis()
# ax.set_xlim(0, 500)
# ax.set_yscale('log')
# ax.set_ylim(0.1, 100)
# ax.set_ylabel('PGA (%g)')
# ax.set_xlabel('Distance (km)')
# plt.legend(loc='upper right')
# plt.tight_layout(rect=(0, 0, 1, 0.97))
# plt.show()

# region PGA vs Epicentral Distance with polygons!!
# colors = ['r', 'g', 'b']
# fig, ax = plt.subplots(figsize=(12, 12))
# fig.suptitle('Warning Time vs MMI for 3 Different Source Depths')
# # for j in np.linspace(-10, 110, num=13):
# #     ax.axhline(j, c='silver', lw=0.5)
# for i in range(len(eqlist_mini)):
#     eq = eqlist_mini[i]
#     y, x = uf.createPolygon(eq.pga, eq.distances_epi, invert=False)
#     # ax[i].scatter(eq.pga, eq.warning_times_s, s=1, c=colors[i])
#     # ax[i].plot(x, y, c=colors[i], alpha=0.6)
#     ax.fill(x, y, c=colors[i], alpha=0.5, label=eqlabels_mini[i])
# ax.axhline(0, c='k', lw=1)
# # ax.set_xscale('log')
# # ax.invert_xaxis()
# ax.set_xlim(0, 500)
# ax.set_yscale('log')
# ax.set_ylim(0.1, 100)
# ax.set_ylabel('PGA (%g)')
# ax.set_xlabel('Distance (km)')
# plt.legend(loc='upper right')
# plt.tight_layout(rect=(0, 0, 1, 0.97))
# plt.show()
# endregion

# region Warning Time vs PGA at different depths
# colors = ['r', 'g', 'b']
# fig, ax = plt.subplots(3,figsize=(8,12))
# fig.suptitle('Warning Time vs MMI at 5, 50, and 150 km depth')
# for i in range(len(eqlist_mini)):
#     eq = eqlist_mini[i]
#     for j in np.linspace(-10, 110, num=13):
#         ax[i].axhline(j, c='silver', lw=0.5)
#     x, y = uf.createPolygon(eq.mmi, eq.warning_times_s, xscale='lin', step=0.1)
#     # ax[i].scatter(eq.pga, eq.warning_times_s, s=1, c=colors[i])
#     # ax[i].plot(x, y, c=colors[i], alpha=0.6)
#     ax[i].fill(x, y, c=colors[i], alpha=0.5)
#     # ax[i].set_xscale('log')
#     # ax[i].invert_xaxis()
#     ax[i].set_xlim(0, 8)
#     ax[i].set_ylim(-15, 120)
#     ax[i].set_title('Source Depth: {}'.format(eqlabels_mini[i]))
#     ax[i].set_xlabel('MMI')
#     ax[i].set_ylabel('Warning Time (s)')
#     ax[i].axhline(0, c='k', lw=1)
# plt.tight_layout(rect=(0, 0, 1, 0.97))
# plt.savefig('Figures/AncScenario/Warning Time vs MMI at 3 depths (polygons).png')
# plt.show()
# endregion

# region Warning Time vs PGA at different depths but with transparent polygons!!!
colors = ['r', 'g', 'b']
fig, ax = plt.subplots(figsize=(8, 6))
fig.suptitle('Depth Tests: Warning Time vs MMI')
for j in np.linspace(-10, 110, num=13):
    ax.axhline(j, c='silver', lw=0.5)
for i in range(len(eqlist_mini)):
    eq = eqlist_mini[i]
    x, y = uf.createPolygon(eq.mmi, eq.warning_times_s, xscale='lin')
    # ax[i].scatter(eq.pga, eq.warning_times_s, s=1, c=colors[i])
    # ax[i].plot(x, y, c=colors[i], alpha=0.6)
    ax.fill(x, y, c=colors[i], alpha=0.5, label=eqlabels_mini[i])
ax.axhline(0, c='k', lw=1)
# ax.set_xscale('log')
# ax.invert_xaxis()
ax.set_xlim(2.5, 8)
ax.set_ylim(-15, 120)
ax.set_xlabel('MMI')
ax.set_ylabel('Warning Time (s)')
plt.legend(loc='upper right')
# plt.tight_layout(rect=(0, 0, 1, 0.99))
plt.savefig('Figures/AncScenario/Warning Time vs MMI at 3 depths (polygons).png')
plt.show()
# endregion

# region Warning Time vs MMI at different depths
colors = ['r', 'g', 'b']
fig, ax = plt.subplots(figsize=(8, 6))
fig.suptitle('Depth Tests: Warning Time vs MMI')
for j in np.linspace(-10, 110, num=13):
    ax.axhline(j, c='silver', lw=0.5)
for i in range(len(eqlist_mini)):
    eq = eqlist_mini[i]
    x, y = uf.createPolygon(eq.mmi, eq.warning_times_s, xscale='lin')
    ax.scatter(eq.mmi, eq.warning_times_s, s=1, c=colors[i])
    ax.plot(x, y, c=colors[i], alpha=0.6)
    # ax.fill(x, y, c=colors[i], alpha=0.5, label=eqlabels_mini[i])
ax.axhline(0, c='k', lw=1)
# ax.set_xscale('log')
# ax.invert_xaxis()
ax.set_xlim(2.5, 8)
ax.set_ylim(-15, 120)
ax.set_xlabel('MMI')
ax.set_ylabel('Warning Time (s)')
plt.legend(loc='upper right')
plt.tight_layout(rect=(0, 0, 1, 0.97))
plt.savefig('Figures/AncScenario/Warning Time vs MMI at 3 depths')
plt.show()
# endregion

# region Warning time Vs Source depth
# # get all points between a and b distance away (a ring around epicenter)
# index_250km = np.where((anc_05.distances_epi > 249) & (anc_05.distances_epi < 251))
# index_175km = np.where((anc_05.distances_epi > 174) & (anc_05.distances_epi < 176))
# index_100km = np.where((anc_05.distances_epi > 99) & (anc_05.distances_epi < 101))
# index_50km = np.where((anc_05.distances_epi > 49) & (anc_05.distances_epi < 51))
# index_10km = np.where((anc_05.distances_epi > 9) & (anc_05.distances_epi < 11))
#
# indices = [index_10km, index_50km, index_100km, index_175km, index_250km]
# rings = {}
# for i in range(len(indices)):
#     rings[i] = anc_05.distances_epi[indices[i]]
# # print(rings.keys(), rings.values())
# # get the warning times on those rings at each depth to test
# # for each ring, get the warning times at each depth and save as a big array
# warning_times = {}
# for i in range(len(indices)):
#     warning_times[i] = [anc_05.warning_times_s[indices[i]], anc_25.warning_times_s[indices[i]],
#                         anc_50.warning_times_s[indices[i]], anc_75.warning_times_s[indices[i]],
#                         anc_100.warning_times_s[indices[i]], anc_125.warning_times_s[indices[i]],
#                         anc_150.warning_times_s[indices[i]]]
#
# colors = ['red', 'lime', 'aqua', 'blue', 'magenta']
# plt.figure(figsize=(12, 8))
# plt.axhline(0, c='k', lw=2)
#
# for i in range(len(indices)):
#     c = colors[i]
#     means = []
#     for j in range(len(depths)):
#         # x will be one value (depth), but needs to be same size as warnign times
#         x = depths[j]*np.ones(warning_times[i][j].shape)
#         # y is the warning times
#         y = warning_times[i][j]
#         plt.scatter(x, y, c=c, s=50)
#         plt.scatter(depths[j], np.mean(y), c='k', s=20, marker='x')
#         means.append(np.mean(y))
#     plt.plot(depths, means, c='k', lw=1, ls='--')
# plt.xlabel('Source Depth (km)')
# plt.ylabel('Warning Time (s)')
# plt.title('Warning Times Vs Source Depth at 10, 50, 100, 175, 250 km away')
# plt.savefig('Figures/AncScenario/Warning Times Vs Source Depth.png')
# plt.show()
# endregion

# wt_50km = [anc_05.warning_times_s[index_50km], anc_25.warning_times_s[index_50km], anc_50.warning_times_s[index_50km],
#            anc_75.warning_times_s[index_50km], anc_100.warning_times_s[index_50km], anc_125.warning_times_s[index_50km],
#            anc_150.warning_times_s[index_50km]]
# wt_50_05 = anc_05.warning_times_s[index_50]
# wt_50_25 = anc_25.warning_times_s[index_50]
# wt_50_50 = anc_50.warning_times_s[index_50]
# wt_50_75 = anc_75.warning_times_s[index_50]
# wt_50_100 = anc_100.warning_times_s[index_50]
# wt_50_125 = anc_125.warning_times_s[index_50]
# wt_50_150 = anc_150.warning_times_s[index_50]
# print(wt_50_25)

# fig, ax = plt.subplots(len(eqlist), figsize=(8, 10))
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
# plt.figure()
# for i in range(len(eqlist)):
#     # x will be one value (depth), but needs to be same size as warnign times
#     x = depths[i]*np.ones(wt_50km[i].shape)
#     # y is the warning times
#     y = wt_50km[i]
#     plt.scatter(x, y, c='k')
#     plt.plot(depths[i], np.mean(y), 'r*')
# plt.xlabel('Source Depth (km)')
# plt.ylabel('Warning Time at ~50 km (s)')
# plt.title('Warning Times at ~50 km Vs Source Depth')
# plt.show()
#
#
# plt.rcParams['font.size'] = '16'
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
