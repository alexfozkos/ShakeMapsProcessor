import numpy as np
import UsefulFunctions as uf
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 28})

Anchorage = uf.Earthquake('Data/Anchorage_grid.xml')
rng = np.random.default_rng()

noise = 0.1 * rng.random(Anchorage.mmi.shape) - 0.05
Anchorage_noisy_mmi = Anchorage.mmi + noise

# calculate rounded mmis
# print(Anchorage.mmi.shape)
rounded_mmi = np.array(Anchorage.mmi, dtype=str)
# print(rounded_mmi.shape)
for i in range(0, rounded_mmi.shape[0]):
    rounded_mmi[i] = rounded_mmi[i, 0][0]
rounded_mmi = np.array(rounded_mmi, dtype=int)


path = './Figures/AnchorageExamples/'  # path to figures folder

# Shaking vs epicentral distance
title = 'Shaking (MMI) vs Distance from epicenter (km)'
plt.figure(figsize=(12,12))
plt.scatter(x=Anchorage.distances_epi, y=rounded_mmi, s=1, c=rounded_mmi)
plt.xlabel('Distance from epicenter (km)')
plt.ylabel('MMI')
plt.xlim(0, 250)
plt.suptitle(title)
plt.savefig(path+title+'.png')

plt.clf()

# Shaking vs average epicentral distance
# recombine the data so we can sort both by mmi
sorted_pairs = np.hstack((Anchorage.distances_epi, rounded_mmi))
# sort both by increasing rounded mmi
sorted_pairs = sorted_pairs[sorted_pairs[:, 1].argsort()]
average_distances = np.array([])
tmp = np.array([])
mmi_current = np.min(rounded_mmi)
for i in range(0, sorted_pairs.shape[0]):
    if sorted_pairs[i, 1] == mmi_current:
        tmp = np.append(tmp, sorted_pairs[i, 0])
    else:
        average_distances = np.append(average_distances, np.mean(tmp))
        tmp = np.array(sorted_pairs[i, 0])
        # print(mmi_current, average_distances)
        mmi_current += 1
    # catch the last mmi bracket
    if i == sorted_pairs.shape[0]-1:
        tmp = np.append(tmp, sorted_pairs[i, 0])
        average_distances = np.append(average_distances, np.mean(tmp))
        # print(mmi_current, average_distances)

y = np.arange(np.min(rounded_mmi), np.max(rounded_mmi)+1, 1)
title = 'Shaking (MMI) vs Average Distance from epicenter (km)'
plt.figure(figsize=(12,12))
plt.plot(average_distances, y, c='k')
plt.xlabel('Distance from epicenter (km)')
plt.ylabel('MMI')
plt.xlim(0, 250)
plt.suptitle(title, fontsize=24)
plt.savefig(path+title+'.png')

plt.clf()


# Warning Time Vs Distance plots
# n = 1
#
# fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 12))
# fig.suptitle('Warning Times Vs Hypocentral Distance')
# z1 = ax1.scatter(Anchorage.distances_hypo[::n], Anchorage.warning_times_s[::n], s=0.1, c=Anchorage.mmi[::n], marker=',', cmap='rainbow')
# ax1.set_xlabel('Hypocentral Distance (km)')
# ax1.set_ylabel('Warning Time (s)')
# ax1.title.set_text('Anchorage')
# ax1.axhline(y=0, ls='--', c='black')
# plt.colorbar(z1, label='MMI', ax=ax1)
#
# z2 = ax2.scatter(Iniskin.distances_hypo[::n], Iniskin.warning_times_s[::n], s=0.1, c=Iniskin.mmi[::n], marker=',', cmap='rainbow')
# ax2.set_xlabel('Hypocentral Distance (km)')
# ax2.set_ylabel('Warning Time (s)')
# ax2.title.set_text('Iniskin')
# ax2.axhline(y=0, ls='--', c='black')
# plt.colorbar(z2, label='MMI', ax=ax2)
#
# fig.tight_layout()
# plt.savefig('Figures/Iniskin Vs Anchorage/Iniskin Vs Anchorage WT-Dist.png')
#
# plt.clf()
#
# # Warning Times vs MMI Double plot
# plt.rcParams.update({'font.size': 15})
# # might be worth it to decimate the data randomly rather than in order?
# n = 5  # plot every nth point
# fig, ax1 = plt.subplots(figsize=(16, 12))
#
# ax1.title.set_text('MMI vs Warning Time, Anchorage and Iniskin (every {} data points)'.format(n))
# ax1.set_xlabel('Warning Time (s)')
# ax1.set_ylabel('MMI')
# ax1.scatter(x=Anchorage.warning_times_s[::n], y=Anchorage_noisy_mmi[::n], c='red', s=0.8, label='Anchorage')
# ax1.scatter(x=Iniskin.warning_times_s[::n], y=Iniskin_noisy_mmi[::n], c='blue', s=0.8, label='Iniskin')
# # ax1.set_xlim(-uf.Earthquake.ttp, 60-uf.Earthquake.ttp)
#
# ax1.axvline(x=0, color='black', lw=3, c='maroon', label='0 Second Warning Time Threshold')
# ax1.axvline(x=5, color='black', lw=3, ls='dashed', label='5 Second Warning Time Threshold')
# ax1.axvline(x=10, color='black', lw=3, ls='dotted', label='10 Second Warning Time Threshold')
#
# plt.legend()
# # plt.legend(loc=3)
# plt.savefig('Figures/Iniskin Vs Anchorage/Iniskin Vs Anchorage MMI-WT')


