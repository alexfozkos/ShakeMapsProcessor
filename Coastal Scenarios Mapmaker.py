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


def km2lat(d):
    return d/110.574


def km2lon(d, lat):
    return d/(111.320*cos(np.deg2rad(lat)))


def createPlane(lon0, lat0, Mw, D, strike, dip, mech):
    #
    #                    1
    #
    #                           2
    #
    #           8                       3
    #
    #                 '0'
    #
    #   7                      4
    #
    #          6
    #
    #                 5

    theta = np.deg2rad(dip)  # convert dip to radians
    angle = np.deg2rad(360 - strike + 90)  # Convert strike to positive angle from x axis, and to radians
    if mech == 'int':  # Table 2, interfrace rupture
        L = 10 ** (-2.90 + 0.63 * Mw)  # km, length of fault
        WL = 10**(0.39 + 0.74 * np.log10(L))  # km, width of fault
        W1 = 10**(-0.86 + 0.35*Mw)
        W = 10**(-1.91 + 0.48*Mw)  # W2
        Wproj = W * cos(theta)  # find the projected width of the fault
        deld = 0.5 * W * sin(theta)  # find the change in depth from the center to the top/bottom of the fault
    elif mech == 'ss':  # Table 5, strike slip rupture
        L = 10 ** (-2.81 + 0.63 * Mw)  # km, length of fault
        W_L = 10 ** (-0.22 + 0.74 * np.log10(L))  # km, width of fault
        W = 10**(-1.39 + 0.35*Mw)
        Wproj = W * cos(theta)  # find the projected width of the fault
        deld = 0.5 * W * sin(theta)  # find the change in depth from the center to the top/bottom of the fault
    elif mech == 'r':  # Table 2 in drive? reverse fault
        L = 10 ** (-2.693 + 0.614 * Mw)  # km, length of fault
        W = 10 ** (-1.669 + 0.435 * Mw)
        Wproj = W * cos(theta)  # find the projected width of the fault
        deld = 0.5 * W * sin(theta)  # find the change in depth from the center to the top/bottom of the fault
    else:
        L = 1
        W = 1
        Wproj = W * cos(theta)
        deld = 0.5 * W * sin(theta)

    print('''Fault Plane Parameters
    Strike: {}
    Dip: {}
    Length: {}
    Width: {}
    Projected Width: {}
    Lower depth: {}
    Upper depth: {}
    '''.format(strike, dip, L, W, Wproj, D+deld, D-deld))
    # calculate points of the plane, midpoints first
    x2 = 0.5 * L * cos(angle - pi)
    lon2 = lon0 + km2lon(x2, lat0)
    y2 = 0.5 * L * sin(angle - pi)
    lat2 = lat0 + km2lat(y2)
    d2 = D
    p2 = (lon2, lat2, d2)

    x6 = 0.5 * L * cos(angle)
    lon6 = lon0 + km2lon(x6, lat0)
    y6 = 0.5 * L * sin(angle)
    lat6 = lat0 + km2lat(y6)
    d6 = D
    p6 = (lon6, lat6, d6)

    x8 = 0.5 * Wproj * cos(angle - pi/2)
    lon8 = lon0 + km2lon(x8, lat0)
    y8 = 0.5 * Wproj * sin(angle - pi/2)
    lat8 = lat0 + km2lat(y8)
    d8 = D + deld
    p8 = (lon8, lat8, d8)

    x4 = 0.5 * Wproj * cos(angle + pi/2)
    lon4 = lon0 + km2lon(x4, lat0)
    y4 = 0.5 * Wproj * sin(angle + pi/2)
    lat4 = lat0 + km2lat(y4)
    d4 = D - deld
    p4 = (lon4, lat4, d4)

    # Corners, use midpoints as reference
    x1 = 0.5 * L * cos(angle - pi)
    lon1 = lon8 + km2lon(x1, lat0)
    y1 = 0.5 * L * sin(angle - pi)
    lat1 = lat8 + km2lat(y1)
    d1 = D + deld
    p1 = (lon1, lat1, d1)

    x7 = 0.5 * L * cos(angle)
    lon7 = lon8 + km2lon(x7, lat0)
    y7 = 0.5 * L * sin(angle)
    lat7 = lat8 + km2lat(y7)
    d7 = D + deld
    p7 = (lon7, lat7, d7)

    x3 = 0.5 * L * cos(angle - pi)
    lon3 = lon4 + km2lon(x3, lat0)
    y3 = 0.5 * L * sin(angle - pi)
    lat3 = lat4 + km2lat(y3)
    d3 = D - deld
    p3 = (lon3, lat3, d3)

    x5 = 0.5 * L * cos(angle)
    lon5 = lon4 + km2lon(x5, lat0)
    y5 = 0.5 * L * sin(angle)
    lat5 = lat4 + km2lat(y5)
    d5 = D - deld
    p5 = (lon5, lat5, d5)

    p0 = (lon0, lat0, D)
    x = [x1, x2, x3, x4, x5, x6, x7, x8]
    y = [y1, y2, y3, y4, y5, y6, y7, y8]
    points = [p0, p1, p2, p3, p4, p5, p6, p7, p8]
    # for point in points:
    #     print(point)
    # print(x)
    # print(y)
    return points


def fixlons(df):
    df['lon'][df['lon'] > 180] -= 360  # convert lons past 180 to negative western lons
    return df


contours_20_1 = pd.read_csv('Data/alu_slab/contour20_1', names=['lon', 'lat', 'depth'])
contours_20_2 = pd.read_csv('Data/alu_slab/contour20_2', names=['lon', 'lat', 'depth'])
contours_20_3 = pd.read_csv('Data/alu_slab/contour20_3', names=['lon', 'lat', 'depth'])

alu_hypocenters = pd.read_csv('Data/Southern Alaska Coast/ALU_hypocenters.txt', delimiter='\t', names=['lon', 'lat', 'depth', 'dip', 'strike'])
alu_hypocenters = fixlons(alu_hypocenters)
qcf_hypocenters = pd.read_csv('Data/Southern Alaska Coast/QCF_hypocenters.txt', delimiter='\t', names=['lon', 'lat', 'depth', 'dip', 'strike'])
cse_hypocenters = pd.read_csv('Data/Southern Alaska Coast/CSE_hypocenters.txt', delimiter='\t', names=['lon', 'lat', 'depth', 'dip', 'strike'])

with open('Data/Southern Alaska Coast/Community Data.json') as json_file:
    comm_dict = json.load(json_file)

title = r"Alaska Southern Coast Scenarios"
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
fig = pygmt.Figure()
# fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
fig.basemap(region='197/51.5/230/63+r', projection='M15c')
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1', land='gainsboro', map_scale='n0.5/0.05+w500+f+u')  # draw coast over datawater='skyblue'

fig.plot(  # Plot seismic stations as triangles
    x=uf.ActiveBBs['lon'],
    y=uf.ActiveBBs['lat'],
    style='t+0.18c',
    color='white',
    pen='0.1p,black',
)
# fig.grdimage(
#     grid='Data/alu_slab/alu_slab2_dip_02.23.18.grd'
# )
# fig.plot(
#     x=contours_20_1['lon'],
#     y=contours_20_1['lat'],
#     pen='0.75p,firebrick',
# )
# fig.plot(
#     x=contours_20_2['lon'],
#     y=contours_20_2['lat'],
#     pen='0.75p,firebrick',
# )
# fig.plot(
#     x=contours_20_3['lon'],
#     y=contours_20_3['lat'],
#     pen='0.75p,firebrick',
# )

starsize = 1
numsize = 0.35
ruptpen = 0.5
starpen = 0.75
planes = {}
# plot rupture proj
for index, row in alu_hypocenters.iterrows():
    p = createPlane(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'int')
    planes[index+1] = p
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        color='red',
        transparency='75',
        # pen=f'{ruptpen}p,red'
    )
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        pen=f'{ruptpen}p,black'
    )
for index, row in cse_hypocenters.iterrows():
    p = createPlane(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'r')
    planes[index+13] = p
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        color='purple',
        transparency='75',
        # pen=f'{ruptpen}p,purple'
    )
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        pen=f'{ruptpen}p,black'
    )
for index, row in qcf_hypocenters.iterrows():
    p = createPlane(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'ss')
    planes[index+15] = p
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        color='green3',
        transparency='25',
        # pen=f'{ruptpen}p,green3'
    )
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        pen=f'{ruptpen}p,green3',
        transparency='25',
    )
# plot stars and numbers
for index, row in alu_hypocenters.iterrows():
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

for index, row in cse_hypocenters.iterrows():
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'a{starsize}c',
        color='white',
        pen=f'{starpen}p,purple'
    )
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'l{numsize}c+t"{index+14}"',
        color='black'
    )

for index, row in qcf_hypocenters.iterrows():
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'a{starsize}c',
        color='white',
        pen=f'{starpen}p,green3'
    )
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'l{numsize}c+t"{index+16}"',
        color='black'
    )
# plot communities
for name, data in comm_dict.items():
    fig.plot(
        x=data['latlon'][1],
        y=data['latlon'][0],
        style='c0.08c',
        color='black'
    )
    if name.lower() in ['sitka', 'sand point']:
        corner = 'BL'
    else:
        corner = 'BR'
    fig.text(
        x=data['latlon'][1],
        y=data['latlon'][0]+0.05,
        text=name,
        font='8p,Helvetica-Narrow-Bold,black,=0.4p,white',
        justify=corner
    )


fig.savefig('Figures/CoastalScenarios/ScenarioMap_notitle.png', dpi=700)
fig.savefig('Figures/CoastalScenarios/ScenarioMap_notitle.pdf', dpi=700)
