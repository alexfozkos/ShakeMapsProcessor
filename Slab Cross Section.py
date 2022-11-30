import numpy as np
import pygmt
import UsefulFunctions as uf
import pandas as pd
import matplotlib.pyplot as plt
import json
MAG = 7.8

sample_points = pd.read_csv('Data/Down Dip/sample_points_full.txt', delimiter=' ', comment='#')
print(sample_points)
slab2path = 'Data/Down Dip/Closest_slab2.txt'
slab2 = pd.read_csv(slab2path)
slab2 = slab2.round(decimals=2)
slab2 = slab2.drop('OBJECTID', axis=1)
slab2projected = pygmt.project(data=slab2,
                               center='-149.955/61.346',
                               azimuth=130,
                               unit=True)

A_p = sample_points['p'].min()  # minimum p value to subtract to that we can draw a cross section A to A', with A at 0 km
fig, ax = plt.subplots(figsize=(8, 4))
plt.grid(alpha=0.6, zorder=0)
ax.scatter(slab2projected[5]-A_p, -slab2projected[2], s=10, c='dimgray', zorder=3)  # slab outline
# ax.scatter(-A_p, 46.7, marker='*', c='darkblue')
# ax.scatter(sample_points['p']-A_p, y=np.zeros(sample_points['p'].count()), s=30, c='darkred')  # sample points
# for p1 in sample_points['p']:
#     ax.axvline(p1-A_p, lw=1, alpha=0.5, c='darkred', ls=':')

planes = {}
for index, row in sample_points.iterrows():
    plane, [l, w] = uf.createPlane(row['lon'], row['lat'], MAG, row['depth'], row['strike'], row['dip'], row['mech'])
    planes[index] = plane
    if row['mech'] == 'or':
        theta = np.deg2rad(row['dip'])
    else:
        theta = np.deg2rad(-row['dip'])
    delp = .5*w*np.cos(theta)
    deld = .5*w*np.sin(theta)
    print(deld, delp)
    x = np.array([row['p'] - delp, row['p'] + delp])
    y = np.array([row['depth'] - deld, row['depth'] + deld])
    plt.plot(x-A_p, y, c='r', lw=2, zorder=4)
    plt.scatter(row['p']-A_p, row['depth'], s=1100, c='white', marker='*', zorder=5, linewidths=1.5, edgecolors='k')
    plt.text(row['p']-A_p, row['depth']+2, s=str(index+1), fontsize=12, zorder=6, ha='center', va='center')


plt.gca().invert_yaxis()
plt.gca().set_aspect('equal', adjustable='box')
# plt.title('Subduction Cross Section and Scenarios')
plt.ylabel('Depth (km)', fontsize=12)
plt.xlabel('Distance (km)', fontsize=12)
plt.tight_layout()
plt.savefig('Figures/Down Dip/CrossSection_notitle.pdf', dpi=700)
plt.savefig('Figures/Down Dip/CrossSection_notitle.png', dpi=700)
