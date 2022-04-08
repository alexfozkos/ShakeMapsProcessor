import math
import numpy as np
import UsefulFunctions as uf
import json
import matplotlib
matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt

plt.rcParams.update({'font.size': 12})

eq_labels = []
for i in range(1, 14):
    eq_labels.append(f'ALU{i}')
for i in range(1, 3):
    eq_labels.append(f'CSE{i}')
for i in range(1, 11):
    eq_labels.append(f'QCF{i}')

with open('Data/Southern Alaska Coast/Community Data.json') as json_file:
    comm_dict = json.load(json_file)
# print(len(comm_dict.keys()))

plt.rc('axes', titlesize=10, labelsize=8)
plt.rc('xtick', labelsize=6)
plt.rc('ytick', labelsize=6)

fig, ax = plt.subplots(3, 5, figsize=(14, 8))

n = 0
for name, data in comm_dict.items():
    wt, = ax[n // 5, n % 5].plot(data['wt'], marker='o', markersize=0.5, lw=0.3, c='k', ls='--', label='Warning time (s)')
    ax[n // 5, n % 5].set_ylabel('Warning Time (s)')
    ax[n // 5, n % 5].set_title(name)
    ax2 = ax[n // 5, n % 5].twinx()
    pga, = ax2.plot(data['pga'], marker='o', c='r', label='PGA (%g)', markersize=0.5, lw=0.3)
    ax2.set_ylabel('PGA (%g)', c='r')
    ax2.set_yscale('log')

    # ax[n // 5, n % 5].legend(handles=[wt, pga])
    n += 1

plt.suptitle('Community Scenario Data')
plt.tight_layout(rect=[0, 0, 1, 0.98])
plt.show()


# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.plot(ancwt, marker='o', c='k', ls='--', label='Warning Time (s)')
# ax1.set_xlabel('Scenario ID')
# ax1.set_ylabel('Warning Time (s)', c='k')
# ax1.set_xticks(range(len(eqlabels)))
# ax1.set_xticklabels(eqlabels)
# ax2.plot(ancpga, marker='o', c='r', label='PGA (%g)')
# ax2.set_ylabel('PGA (%g)', c='r')
# ax2.set_yscale('log')
# plt.title('Scenario PGA and Warning Times for Anchorage')
# # plt.legend()
# plt.show()
