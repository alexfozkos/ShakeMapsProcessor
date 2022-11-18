import numpy as np
import pygmt
import UsefulFunctions as uf
import pandas as pd
import matplotlib.pyplot as plt
import json

slab2path = 'Data/Down Dip/Closest_slab2.txt'
slab2 = pd.read_csv(slab2path)
slab2 = slab2.round(decimals=2)
slab2 = slab2.drop('OBJECTID', axis=1)
slab2projected = pygmt.project(data=slab2,
                               center='-149.955/61.346',
                               azimuth=130,
                               unit=True)

invl = 50
sample_points_top = pygmt.project(generate=f'{invl}',
                                  center='-149.955/61.346',
                                  azimuth=130,
                                  unit=True,
                                  length=[-4*invl, 0])
sample_points_bot = pygmt.project(generate=f'{invl}',
                                  center='-149.955/61.346',
                                  azimuth=130,
                                  unit=True,
                                  length=[invl, 8*invl])

sample_points = pd.concat([sample_points_top, sample_points_bot], ignore_index=True, axis=0)
sample_points.to_csv('Data/Down Dip/sample_points.txt', sep=' ', float_format='%.3f')
slab2projected.to_csv('Data/Down Dip/slab2_projected.txt', sep=' ', float_format='%.3f')
print(slab2projected[6].max())
# print(slab2.info)
# print(slab2projected.info)
# print(sample_points_top)
# print(sample_points_bot)

title = r"Slab Scenarios"
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
fig = pygmt.Figure()
# fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
fig.basemap(region='206.5/58/218/63+r', projection='M15c', frame=["af", f'WSne+t"{title}"'])
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1', land='gainsboro')  # draw coast over datawater='skyblue'

fig.plot(  # Plot seismic stations as triangles
    x=uf.ActiveBBs['lon'],
    y=uf.ActiveBBs['lat'],
    style='t+0.13c',
    color='white',
    pen='0.1p,black',
)

fig.plot(
    x=slab2projected[0],
    y=slab2projected[1],
    style='c+0.13c',
    color='black'
)
fig.plot(
    x=slab2projected[7],
    y=slab2projected[8],
    style='c+0.13c',
    color='green'
)
fig.plot(
    x=sample_points_top['r'],
    y=sample_points_top['s'],
    style='c+0.13c',
    color='red'
)
fig.plot(
    x=sample_points_bot['r'],
    y=sample_points_bot['s'],
    style='c+0.13c',
    color='red'
)
fig.plot(
    x=-149.955,
    y=61.346,
    style='c+0.17c',
    color='blue',
    transparency=40
)
with open('Data/Southern Alaska Coast/Community Data.json') as json_file:
    comm_dict = json.load(json_file)
# plot communities
for name, data in comm_dict.items():
    fig.plot(
        x=data['latlon'][1],
        y=data['latlon'][0],
        style='c0.08c',
        color='black'
    )
    fig.plot(
        x=data['latlon'][1],
        y=data['latlon'][0] + 0.1,
        style=f'l0.25c+t"{name}"',
        color='black'
    )

fig.savefig('Figures/Down Dip/SlabScenarioMap.pdf')

A_p = sample_points['p'].min()  # minimum p value to subtract to that we can draw a cross section A to A', with A at 0 km
fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(slab2projected[5]-A_p, -slab2projected[2], s=20, c='k')
ax.scatter(-A_p, 46.7, marker='*', c='darkblue')
ax.scatter(sample_points['p']-A_p, y=np.zeros(sample_points['p'].count()), s=30, c='darkred')
for p1 in sample_points['p']:
    ax.axvline(p1-A_p, lw=1, alpha=0.5, c='darkred', ls=':')
plt.gca().invert_yaxis()
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(alpha=0.6)
plt.title('Subduction Cross Section and Scenarios')
plt.ylabel('Depth (km)')
plt.xlabel('Distance (km)')
plt.tight_layout()
plt.savefig('Figures/Down Dip/CrossSection.pdf')
