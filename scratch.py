import math
import numpy as np
import pandas as pd
import UsefulFunctions as uf
import json
import matplotlib
from MMILegend import mmimap, mmi_cmap, draw_colorbar

matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt
from MMILegend import mmimap, mmi_cmap, draw_colorbar

eq = uf.Earthquake('Data/AncScenarioGrids/gridreal.xml')


mmi = eq.mmi
wt = eq.warning_times_s
wt_means = []
wt_medians = []
mmi_vals = np.arange(mmi.min(), mmi.max()+0.1, 0.1)
print(mmi.max())
print(mmi.min())
print(mmi_vals)
rng = np.random.default_rng()
noise = 0.1 * rng.random(mmi.shape) - 0.05
for k in mmi_vals:
    mask = np.isclose(mmi, k)
    wt_means.append(np.mean(wt[mask]))
    wt_medians.append(np.median(wt[mask]))

x_mids, y_points = uf.createPolygon(mmi, wt, xscale='lin', )

fig = plt.figure(figsize=(6, 6))
plt.scatter(mmi+noise, wt, c='k', label='Data', s=0.01, marker='o')
plt.plot(x_mids, y_points, lw=0.5, c='r', label='Cloud Polygon')
plt.plot(mmi_vals, wt_means, lw=2, marker='^', markersize=3, c='g', label='Warning Time Means', alpha=0.9)
plt.plot(mmi_vals, wt_medians, lw=2, marker='s', markersize=3, c='purple', label='Warning Time Medians', alpha=0.9)
plt.ylabel('Warning Time (s)')
plt.xlabel('MMI')
plt.title('Warning Time vs MMI Plot types w/ noise')
plt.xlim(left=2)
plt.ylim(top=200)
plt.axhline(0, ls=':', lw=1, c='gray', alpha=0.8)
plt.legend()
plt.savefig('Figures/Test.png', dpi=700)
