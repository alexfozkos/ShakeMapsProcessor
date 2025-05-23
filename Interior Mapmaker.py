import os
import json
import matplotlib as mpl
import geopandas as gpd
mpl.rcParams["backend"] = "TkAgg"
import pandas as pd
import numpy as np
from numpy import sin, cos, pi
from matplotlib import pyplot as plt
import pygmt
import UsefulFunctions as uf
pygmt.config(MAP_FRAME_TYPE="plain")
pygmt.config(FORMAT_GEO_MAP="ddd.x")

MAG = 7.3
ID = 'INTERIORSCENARIOS'

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
    if mech == 'int':  # Table 2, interface rupture
        L = 10 ** (-2.90 + 0.63 * Mw)  # km, length of fault
        WL = 10 ** (0.39 + 0.74 * np.log10(L))  # km, width of fault
        W1 = 10 ** (-0.86 + 0.35 * Mw)
        W = 10 ** (-1.91 + 0.48 * Mw)  # W2
        Wproj = W * cos(theta)  # find the projected width of the fault
        deld = 0.5 * W * sin(theta)  # find the change in depth from the center to the top/bottom of the fault
    elif mech == 'r':  # Table 2 in drive reverse fault (where did these numbers come from? Investigate)
        L = 10 ** (-2.693 + 0.614 * Mw)  # km, length of fault
        W = 10 ** (-1.669 + 0.435 * Mw)
        Wproj = W * cos(theta)  # find the projected width of the fault
        deld = 0.5 * W * sin(theta)  # find the change in depth from the center to the top/bottom of the fault
    elif mech == 'ss':  # Table 5, strike slip rupture
        L = 10 ** (-2.81 + 0.63 * Mw)  # km, length of fault
        W_L = 10 ** (-0.22 + 0.74 * np.log10(L))  # km, width of fault
        W = 10 ** (-1.39 + 0.35 * Mw)
        Wproj = W * cos(theta)  # find the projected width of the fault
        deld = 0.5 * W * sin(theta)  # find the change in depth from the center to the top/bottom of the fault
    elif mech == 'is':  # Table 5 in drive inslab
        L = 10 ** (-3.03 + 0.63 * Mw)  # km, length of fault
        W = 10 ** (-1.01 + 0.35 * Mw)
        Wproj = W * cos(theta)  # find the projected width of the fault
        deld = 0.5 * W * sin(theta)  # find the change in depth from the center to the top/bottom of the fault
    elif mech == 'or':  # Table 5 outer rise
        L = 10 ** (-2.87 + 0.63 * Mw)  # km, length of fault
        W = 10 ** (-1.18 + 0.35 * Mw)
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


crst_hypocenters = pd.read_csv('Data/Interior Crustal/Crustal_Hypocenters.txt', delimiter='\t',
                               names=['lon', 'lat', 'depth', 'dip', 'strike', 'name'])

gdf = gpd.read_file('Data/faults/mp141/shapefiles/mp141-qflt-line-alaska.shp')
# gdf = gdf.drop(['CODE', 'NUM', 'AGE', 'ACODE', 'SLIPRATE', 'SLIPCODE', 'SLIPSENSE', 'DIPDIRECTI', 'FCODE', 'FTYPE', 'SecondaryS'], axis=1)
searchfor = 'Denali fault|Castle Mountain fault|Northern Foothills fold and thrust belt|seismic zone|Tintina'
linestrings = [geom for geom in gdf[gdf['NAME'].str.contains(searchfor, regex=True)].geometry]
# linestrings = [geom for geom in gdf.geometry]

# all_data = []
# all_data.append(gdf[gdf['NAME'].str.contains(searchfor, regex=True)])
# gdf.plot()
# plt.show()

#region map maker
# title = r"Interior Crustal Scenarios"
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
fig = pygmt.Figure()
# fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
fig.basemap(region='207.5/60.5/217/66.2+r', projection='M15c', frame=None)
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1', land='gainsboro', map_scale='n0.8/0.04+w100+f+u', frame=None)  # draw coast over datawater='skyblue'
ll = 1
data = gdf
# plot faults
for geom in linestrings:
    if geom.type == 'LineString':
        x, y = geom.coords.xy
        fig.plot(x=x, y=y, pen='1p,red4')
    elif geom.type == 'MultiLineString':
        for line in geom.geoms:
            x, y = line.coords.xy
            fig.plot(x=x, y=y, pen='1p,red4')

fig.plot(  # Plot seismic stations as triangles
    x=uf.ActiveBBs['lon'],
    y=uf.ActiveBBs['lat'],
    style='t+0.18c',
    color='white',
    pen='0.1p,black',
)



starsize = 1.1
numsize = 0.4
ruptpen = 0.5
starpen = 0.8
planes = {}
for index, row in crst_hypocenters.iterrows():
    p = createPlane(row['lon'], row['lat'], MAG, row['depth'], row['strike'], row['dip'], 'ss')
    planes[index] = p
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        color='red',
        # transparency='25',
        pen='2p,red'
    )

for index, row in crst_hypocenters.iterrows():
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

with open('Data/Interior Crustal/Old Interior Community Data.json') as json_file:
    comm_dict = json.load(json_file)
# plot communities
for name, data in comm_dict.items():
    if name in ['North Pole', 'Eielson Air Force Base', 'Clear Space Force Station', 'Fort Wainwright']:
        continue
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
        font='14p,Helvetica-Narrow-Bold,black,=0.6p,white',
        justify=corner
    )

fig.savefig('Figures/Interior Crustal/InteriorScenarioMap_notitle.pdf')
fig.savefig('Figures/Interior Crustal/InteriorScenarioMap_notitle.png', dpi=700)

#endregion map maker
