import UsefulFunctions as uf
import numpy as np
import collections
from matplotlib import pyplot as plt

eq = uf.Earthquake('Data/AncScenarioGrids/gridreal.xml')

mmi_min = np.min(eq.mmi)
mmi_max = np.max(eq.mmi)
# every nth point
n = 1
# Create array of warning times and mmi for each point
points = np.hstack((eq.warning_times_s[::n], eq.mmi[::n]))
# Sort the points by mmi
points = points[np.argsort(points[:, 1])]
# Create a dictionary where key=mmi (major), each value is an vertically stacked array of [warning time]
# for each point
point_dict = {}

for i in points:
    key = int(str(i[1])[0])
    if key not in point_dict.keys():
        point_dict[key] = np.array(i[0])
        pass
    else:
        point_dict[key] = np.append(point_dict[key], i[0])

# region Histogram Plotter for Anchorage 2018
figure, ax = plt.subplots(nrows=2, ncols=4, figsize=(20, 13))
k = 0
for i in range(0, 2):
    for j in range(0, 4):
        if i == 1 and j == 3:
            break
        k += 1
        ax[i, j].grid()
        n, bins, patches = ax[i, j].hist(point_dict[k], bins=10)
        ax[i, j].set_xlabel('Warning Time (s)')
        ax[i, j].set_ylabel('Count')
        ax[i, j].set_title('MMI {} to {}: {} points'.format(k, k + 0.9, point_dict[k].size))
ax[1, 3].grid()
_, _, _ = ax[1, 3].hist(eq.warning_times_s, bins=25)
ax[1, 3].set_xlabel('Warning Time (s)')
ax[1, 3].set_ylabel('Count')
ax[1, 3].set_title('All Points: {} points'.format(eq.warning_times_s.size))
figure.suptitle('Histograms for Anchorage 2018 Earthquake', fontsize=30)
plt.tight_layout()
plt.subplots_adjust(top=0.93)
plt.savefig('Figures/cdfs/Histogram for Anchorage 2018.png'.format(k, k + 0.9))
#endregion


# region create PDF and CDF for each major MMI in the dictionary (1, 2, 3 ...)
# create PDF and CDF for each major MMI in the dictionary (1, 2, 3 ...)
# for k in point_dict.keys():
#     # getting data of the histogram
#     count, bins_count = np.histogram(point_dict[k], bins=10)
#
#     # finding the PDF of the histogram using count values
#     pdf = count / sum(count)
#
#     # using numpy np.cumsum to calculate the CDF
#     # We can also find using the PDF values by looping and adding
#     cdf = np.cumsum(pdf)
#
#     # plotting PDF and CDF
#     plt.plot(bins_count[1:], pdf, color="red", label="PDF")
#     plt.plot(bins_count[1:], cdf, label="CDF")
#     plt.xlabel('Warning Time (s)')
#     plt.title('MMI {} to {}'.format(k, k + 0.9))
#     plt.legend()
#     plt.grid()
#     plt.savefig('Figures/cdfs/CDF MMI {} to {}.png'.format(k, k + 0.9))
#     plt.clf()
# endregion

# region Plot for percent warning times at least each mmi
# Plot for percent warning times at least each mmi
# plt.figure(figsize=(12, 6))
# for k in point_dict.keys():
#     # getting data of the histogram
#     count, bins_count = np.histogram(point_dict[k], bins=10)
#     # finding the PDF of the histogram using count values
#     pdf = count / sum(count)
#
#     # using numpy np.cumsum to calculate the CDF
#     # We can also find using the PDF values by looping and adding
#     cdf = np.cumsum(pdf)
#
#     # plotting PDF and CDF
#     # plt.plot(bins_count[1:], pdf*100, color="red", label="PDF")
#     plt.plot(bins_count[0:-1], cdf[::-1]*100, label="MMI {} to {}".format(k, k + 0.9))
#     plt.xlabel('Warning Time (s)')
#     plt.ylabel('% of sites')
#     plt.title('Percent of sites with at least X warning time(s) MMI {} to {}'.format(k, k + 0.9))
#     plt.legend()
#     plt.grid()
#     plt.savefig('Figures/cdfs/Minimum WT percentages MMI {} to {}.png'.format(k, k + 0.9))
#     plt.clf()
# endregion
