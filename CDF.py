import UsefulFunctions as uf
import numpy as np
import collections
from matplotlib import pyplot as plt

eq = uf.Earthquake()

mmi_min = np.min(eq.mmi)
mmi_max = np.max(eq.mmi)

# every nth point
n = 1
# Create array of warning times and mmi for each point
points = np.hstack((eq.warning_times[::n], eq.mmi[::n]))
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
    point_dict[key] = np.append(point_dict[key], i[0])

# print(point_dict[5])
#Sorts the dictionary keys by mmi, decreasing (highest mmi keys first)
#point_dict = collections.OrderedDict(reversed(sorted(point_dict.items())))
for k in point_dict.keys():
    # getting data of the histogram
    count, bins_count = np.histogram(point_dict[k], bins=10)

    # finding the PDF of the histogram using count values
    pdf = count / sum(count)

    # using numpy np.cumsum to calculate the CDF
    # We can also find using the PDF values by looping and adding
    cdf = np.cumsum(pdf)

    # plotting PDF and CDF
    plt.plot(bins_count[1:], pdf, color="red", label="PDF MMI %i" % k)
    plt.plot(bins_count[1:], cdf, label="CDF MMI %i" % k)
    plt.xlabel('Warning Time (s)')
    plt.title('MMI %i' % k)
    plt.legend()
    plt.grid()
    plt.savefig('Figures/cdfs/CDF MMI %i' % k)
    plt.clf()

