import os
import json
import matplotlib as mpl

mpl.rcParams["backend"] = "TkAgg"
import pandas as pd
import numpy as np
from numpy import sin, cos, pi
from matplotlib import pyplot as plt
import pygmt
import UsefulFunctions as uf
pygmt.config(MAP_FRAME_TYPE="plain")
pygmt.config(FORMAT_GEO_MAP="ddd.x")

MAG = 7.8
ID = 'SLABSCENARIOS'


def fixlons(df):
    df['lon'][df['lon'] > 180] -= 360  # convert lons past 180 to negative western lons
    return df


dd_hypocenters = pd.read_csv('Data/Down Dip/sample_points_full.txt', delimiter=' ', comment='#')

#region map maker
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
fig = pygmt.Figure()
# fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
fig.basemap(region='206/58.25/217/63+r', projection='M15c', frame=None)
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1', land='gainsboro', map_scale='n0.5/0.05+w200+f+u', frame=None)  # draw coast over datawater='skyblue'

fig.plot(  # Plot seismic stations as triangles
    x=uf.ActiveBBs['lon'],
    y=uf.ActiveBBs['lat'],
    style='t+0.18c',
    color='white',
    pen='0.1p,black',
)

starsize = 1.0
numsize = 0.35
ruptpen = 0.5
starpen = 0.75
planes = {}
for index, row in dd_hypocenters.iterrows():
    p, [l, w] = uf.createPlane(row['lon'], row['lat'], MAG, row['depth'], row['strike'], row['dip'], row['mech'])
    planes[index] = p
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        color='red',
        transparency='75',
        # pen='1p,black'
    )
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        pen=f'{ruptpen}p,black'
    )
for index, row in dd_hypocenters.iterrows():
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'a{starsize}c',
        color='white',
        pen=f'{starpen}p,red'
    )
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'l{numsize}c+t"{index+1}"',
        color='black'
    )

with open('Data/Southern Alaska Coast/Old Community Data.json') as json_file:
    comm_dict = json.load(json_file)
# plot communities
for name, data in comm_dict.items():
    fig.plot(
        x=data['latlon'][1],
        y=data['latlon'][0],
        style='c0.08c',
        color='black'
    )
    if name.lower() in ['anchorage', 'whittier']:
        corner = 'TR'
        adjust = -0.025
    else:
        corner = 'BR'
        adjust = 0.025
    fig.text(
        x=data['latlon'][1],
        y=data['latlon'][0] + adjust,
        text=name,
        font='10p,Helvetica-Narrow-Bold,black,=0.45p,white',
        justify=corner
    )

fig.savefig('Figures/Down Dip/SlabScenarioMap_notitle.png', dpi=700)
fig.savefig('Figures/Down Dip/SlabScenarioMap_notitle.pdf', dpi=700)

#endregion map maker
