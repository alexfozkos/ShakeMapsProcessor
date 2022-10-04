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

MAG = 7.8
ID = 'SLABSCENARIOS'

def km2lat(d):
    return d / 110.574


def km2lon(d, lat):
    return d / (111.320 * cos(np.deg2rad(lat)))


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
        WL = 10 ** (0.39 + 0.74 * np.log10(L))  # km, width of fault
        W1 = 10 ** (-0.86 + 0.35 * Mw)
        W = 10 ** (-1.91 + 0.48 * Mw)  # W2
        Wproj = W * cos(theta)  # find the projected width of the fault
        deld = 0.5 * W * sin(theta)  # find the change in depth from the center to the top/bottom of the fault
    elif mech == 'ss':  # Table 5, strike slip rupture
        L = 10 ** (-2.81 + 0.63 * Mw)  # km, length of fault
        W_L = 10 ** (-0.22 + 0.74 * np.log10(L))  # km, width of fault
        W = 10 ** (-1.39 + 0.35 * Mw)
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
    '''.format(strike, dip, L, W, Wproj, D + deld, D - deld))
    # calculate points of the plane, midpoints first
    x2 = 0.5 * L * cos(angle - pi)
    # print(type(lon0))
    # print(lon0)
    # print(type(km2lon(x2, lat0)))
    lon2 = lon0 + km2lon(x2, lat0)
    y2 = 0.5 * L * sin(angle - pi)
    lat2 = lat0 + km2lat(y2)
    d2 = D
    p2 = (lon2-360, lat2, d2)

    x6 = 0.5 * L * cos(angle)
    lon6 = lon0 + km2lon(x6, lat0)
    y6 = 0.5 * L * sin(angle)
    lat6 = lat0 + km2lat(y6)
    d6 = D
    p6 = (lon6-360, lat6, d6)

    x8 = 0.5 * Wproj * cos(angle - pi / 2)
    lon8 = lon0 + km2lon(x8, lat0)
    y8 = 0.5 * Wproj * sin(angle - pi / 2)
    lat8 = lat0 + km2lat(y8)
    d8 = D + deld
    p8 = (lon8-360, lat8, d8)

    x4 = 0.5 * Wproj * cos(angle + pi / 2)
    lon4 = lon0 + km2lon(x4, lat0)
    y4 = 0.5 * Wproj * sin(angle + pi / 2)
    lat4 = lat0 + km2lat(y4)
    d4 = D - deld
    p4 = (lon4-360, lat4, d4)

    # Corners, use midpoints as reference
    x1 = 0.5 * L * cos(angle - pi)
    lon1 = lon8 + km2lon(x1, lat0)
    y1 = 0.5 * L * sin(angle - pi)
    lat1 = lat8 + km2lat(y1)
    d1 = D + deld
    p1 = (lon1-360, lat1, d1)

    x7 = 0.5 * L * cos(angle)
    lon7 = lon8 + km2lon(x7, lat0)
    y7 = 0.5 * L * sin(angle)
    lat7 = lat8 + km2lat(y7)
    d7 = D + deld
    p7 = (lon7-360, lat7, d7)

    x3 = 0.5 * L * cos(angle - pi)
    lon3 = lon4 + km2lon(x3, lat0)
    y3 = 0.5 * L * sin(angle - pi)
    lat3 = lat4 + km2lat(y3)
    d3 = D - deld
    p3 = (lon3-360, lat3, d3)

    x5 = 0.5 * L * cos(angle)
    lon5 = lon4 + km2lon(x5, lat0)
    y5 = 0.5 * L * sin(angle)
    lat5 = lat4 + km2lat(y5)
    d5 = D - deld
    p5 = (lon5-360, lat5, d5)

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


crst_hypocenters = pd.read_csv('Data/Down Dip/sample_points_full.txt', delimiter=' ')
print(crst_hypocenters.info)
# create rupture geometries
# for index, row in crst_hypocenters.iterrows():
#     p = createPlane(row['lon'], row['lat'], MAG, row['depth'], row['strike'], row['dip'], 'ss')
#     print(f'INDEX: {index}')
#     name = row['name']
#     lat = row['lat']
#     lon = row['lon'] - 360
#     d = row['depth']
#     path1 = f'Data/Interior Crustal/Shakemap Folders/{name}'
#     path2 = f'{path1}/current'
#     if not os.path.exists(path1):
#         os.mkdir(path1)
#     if not os.path.exists(path2):
#         os.mkdir(path2)
#     with open(f'{path2}/event.xml', 'w') as f:  # event file
#         f.write(f'<earthquake id="{ID}" netid="ak" network="Alaska Earthquake Center" lat="{lat}" '
#                 f'lon="{lon}" depth="{d}" mag="{MAG}" time="2022-08-4T21:29:29Z" '
#                 f'locstring="{name}" event_type="SCENARIO"/>')
#     with open(f'{path2}/rupture.json', 'w') as f:  # rupture file
#         f.write(f'{{"metadata": {{"id": "{ID}", "netid": "ak", "network": "Alaska Earthquake Center", '
#                 f'"lat": {lat}, "lon": {lon}, "depth": {d}, "mag": {MAG}, "time": "2022-03-28T21:29:29.000000Z", '
#                 f'"locstring": "{name}", "reference": "Fozkos 2022", "mech": "SS", "rake": 0.0, '
#                 f'"productcode": "{ID}"}}, "features": [{{"geometry": {{"coordinates": '
#                 f'[[[[{p[5][0]}, {p[5][1]}, {p[5][2]}], [{p[3][0]}, {p[3][1]}, {p[3][2]}], [{p[1][0]}, {p[1][1]}, {p[1][2]}], '
#                 f'[{p[7][0]}, {p[7][1]}, {p[7][2]}], [{p[5][0]}, {p[5][1]}, {p[5][2]}]]]], "type": "MultiPolygon"}}, '
#                 f'"properties": {{"rupture type": "rupture extent"}}, "type": "Feature"}}], '
#                 f'"type": "FeatureCollection"}}')
#     with open(f'{path2}/model.conf', 'w') as f:
#         f.write('''# This file (model_select.conf) is generated automatically by the 'select'
# # coremod. It will be completely overwritten the next time select is run. To
# # preserve these settings, or to modify them, copy this file to a file called
# # 'model.conf' in the event's current directory. That event-specific
# # model.conf will be used and model_select.conf will be ignored. (To avoid
# # confusion, you should probably delete this comment section from your event-
# # specific model.conf.)
# [gmpe_sets]
#     [[gmpe_QCF3_custom]]
#         gmpes = active_crustal_nshmp2014,
#         weights = 1.0,
#         weights_large_dist = None
#         dist_cutoff = nan
#         site_gmpes = None
#         weights_site_gmpes = None
# [modeling]
#     gmpe = gmpe_QCF3_custom
#     mechanism = SS
#     ipe = VirtualIPE
#     gmice = WGRW12
#     ccf = LB13''')

# Create PyGMT map of scenarios
#region map maker
title = r"Interior Crustal Scenarios"
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
fig = pygmt.Figure()
# fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
fig.basemap(region='206.5/60.5/218/63+r', projection='M15c', frame=["af", f'WSne+t"{title}"'])
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1', land='gainsboro')  # draw coast over datawater='skyblue'

fig.plot(  # Plot seismic stations as triangles
    x=uf.ActiveBBs['lon'],
    y=uf.ActiveBBs['lat'],
    style='t+0.13c',
    color='white',
    pen='0.1p,black',
)

starsize = 1.0
numsize = 0.45
# numsize2 = 0.25
planes = {}
for index, row in crst_hypocenters.iterrows():
    p = createPlane(row['lon'], row['lat'], MAG, row['depth'], row['strike'], row['dip'], row['mech'])
    planes[index] = p
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        color='black',
        transparency='25',
        pen='1p,black'
    )
    # fig.plot(
    #     x=p[0][0],
    #     y=p[0][1],
    #     style=f'a{starsize}c',
    #     color='white',
    #     pen='0.25p,red'
    # )
    # fig.plot(
    #     x=p[0][0],
    #     y=p[0][1],
    #     style=f'l{numsize}c+t"{index + 1}"',
    #     color='black'
    # )
for index, row in crst_hypocenters.iterrows():
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'a{starsize}c',
        color='white',
        pen='0.25p,red'
    )

    if index < 9:
        numsize2 = numsize
    else:
        numsize2 = numsize - 0.05

    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'l{numsize2}c+t"{index+1}"',
        color='black'
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
fig.savefig('Figures/Interior Crustal/InteriorScenarioMap.pdf')
#endregion map maker
