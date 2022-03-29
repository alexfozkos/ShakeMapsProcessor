import matplotlib as mpl
mpl.rcParams["backend"] = "TkAgg"
import pandas as pd
import numpy as np
from numpy import sin, cos, pi
from matplotlib import pyplot as plt
import pygmt
import UsefulFunctions as uf


# Magnitude
# Mw = 8.3
# Allen & Hayes, 2017, Table 2 "Interface-Rupture-Scaling Coefficients Determined from Orthogonal Regression"
# L = 10**(-2.90 + 0.63*Mw)  # km
# W1 = 10**(-0.86 + 0.35*Mw)  # km
# W2 = 10**(-1.91 + 0.48*Mw)  # km
# S1 = 10**(-3.63 + 0.96*Mw)  # km^2
# S2 = 10**(-5.62 + 1.22*Mw)  # km^2
# DMAX = 10**(-4.94 + 0.71*Mw)  # m
# DAV = 10**(-5.05 + 0.66*Mw)  # m
# W = 10**(0.39 + 0.74 * np.log10(L))  # km


def km2lat(d):
    return d/110.574


def km2lon(d, lat):
    return d/(111.320*cos(np.deg2rad(lat)))


def createPlane(lon0, lat0, Mw, D, strike, dip):
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
    L = 10 ** (-2.90 + 0.63 * Mw)  # km, length of fault
    W = 10**(0.39 + 0.74 * np.log10(L))  # km, width of fault
    Wproj = W * cos(theta)  # find the projected width of the fault
    deld = 0.5 * W * sin(theta)  # find the change in depth from the center to the top/bottom of the fault
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


dep = pd.read_csv('Data/alu_slab/alu_slab2_dep_02.23.18.xyz', names=['lon', 'lat', 'depth'])
dip = pd.read_csv('Data/alu_slab/alu_slab2_dip_02.23.18.xyz', names=['lon', 'lat', 'dip'])
str = pd.read_csv('Data/alu_slab/alu_slab2_str_02.23.18.xyz', names=['lon', 'lat', 'strike'])
contours_20_1 = pd.read_csv('Data/alu_slab/contour20_1', names=['lon', 'lat', 'depth'])
contours_20_2 = pd.read_csv('Data/alu_slab/contour20_2', names=['lon', 'lat', 'depth'])
contours_20_3 = pd.read_csv('Data/alu_slab/contour20_3', names=['lon', 'lat', 'depth'])

data = pd.concat([dep, dip['dip'], str['strike']], axis=1)

# Clean up data
data = data.dropna()  # drop nan's
# Saves data as a text file
# np.savetxt('Data/alu_slab_data.csv', data.values, fmt='%.4f', delimiter=',')
# Converts positve lon data above 180 into negative western notation
# data = fixlons(data)

# contours_20_1 = fixlons(contours_20_1)
# contours_20_2 = fixlons(contours_20_2)
# contours_20_3 = fixlons(contours_20_3)

# depth_series = pd.Series(dep['depth'])
# depth_series = depth_series.values
# depth_grid = depth_series.reshape(int(depth_series.shape[0]/1301), 1301)

# data.plot(x='lon', y='lat', kind='scatter', c='depth', title='test')
# plt.plot(contours_20_1['lon'], contours_20_1['lat'], c='b',)
# plt.plot(contours_20_2['lon'], contours_20_2['lat'], c='k',)
# plt.plot(contours_20_3['lon'], contours_20_3['lat'], c='r',)
# plt.show()

# points = createplane(-160, 53, 8.3, 20, 45, 8)
# colors = ['k','r','orange','yellow','green','blue','cyan','purple','pink']
# plt.figure()
# i = 0
# for p in points:
#     plt.plot(p[0], p[1], c=colors[i], marker='*', markersize=10)
#     i += 1
# plt.show()

# title = r"Slab 2 mapping"
# coast_border = "a/0.5p,brown"
# shorelines = "0.3p,black"
# fig = pygmt.Figure()
# # fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
# fig.basemap(region='180/49/240/62+r', projection='M15c', frame=["af", f'WSne+t"{title}"'])
# fig.coast(shorelines=shorelines, borders=coast_border, water='skyblue', land='lightgray')  # draw coast over datawater='skyblue'
#
# # fig.plot(  # Plot seismic stations as triangles
# #     x=uf.ActiveBBs['lon'],
# #     y=uf.ActiveBBs['lat'],
# #     style='t+0.3c',
# #     color='white',
# #     pen='black',
# # )
# fig.grdimage(
#     grid='Data/alu_slab/alu_slab2_dip_02.23.18.grd'
# )
# fig.savefig('Figures/misc/PyGMTMap.png')

hypocenters = pd.read_csv('Data/alu_slab/Hypocenters.txt', delimiter='\t', names=['lon', 'lat', 'depth', 'dip', 'strike'])
print(hypocenters.info())
planes = {}

with open('Data/alu_slab/Alu_geometries.txt', 'w') as w:
    w.write("Lon, Lat, Depth\n")
    for index, row in hypocenters.iterrows():
        p = createPlane(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'])
        planes[index] = p
        corners= [p[1], p[3], p[5], p[7]]
        w.write("Alu Index {}\nCenter: [{:.2f}, {:.2f}, {:.4f}]\n".format(index+1, *p[0]))
        w.write("Strike: {}\nDip: {}\n".format(row['strike'], row['dip']))
        for corner in corners:
            w.write("[{:.2f}, {:.2f}, {:.4f}]\n".format(*corner))
        w.write("\n")

