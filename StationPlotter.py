import pygmt
import numpy as np
datapath = './Data/Iniskin_nearfield.gmtvec'
station_names = np.genfromtxt(datapath, usecols=[7], dtype=str)
dn = np.genfromtxt(datapath, usecols=[3], dtype=float) *100
de = np.genfromtxt(datapath, usecols=[2], dtype=float) *100
lon = np.genfromtxt(datapath, usecols=[0], dtype=float)
lat = np.genfromtxt(datapath, usecols=[1], dtype=float)
sige = np.genfromtxt(datapath, usecols=[4], dtype=float)
sign = np.genfromtxt(datapath, usecols=[5], dtype=float)
mag = np.sqrt(dn**2 + de**2)
print(np.max(mag), np.min(mag))
print(dn[:3], de[:3])

# Create a plot with coast, Mercator projection (M) over the continental US
fig = pygmt.Figure()
fig.coast(
    region=[np.min(lon)-1, np.max(lon)+1, np.min(lat)-0.5, np.max(lat)+0.5],
    projection="M10c",
    frame=["ag",'+t"GPS Station Map"'],
    borders=1,
    shorelines="0.25p,black",
    area_thresh=4000,
    land="grey",
    water="lightblue",
)
#plot epicenter
fig.plot(
    x=-153.339,
    y=59.620,
    style='a0.5c',
    pen='0.75p,black',
    color='magenta'
)
# plot stations as red triangles
fig.plot(
    x=lon,
    y=lat,
    style='t0.3c',
    pen='0.75p,black',
    color='red'
)
# Plot a vector using the x, y, direction parameters
style = "v0.25c+ea+a45"
fig.plot(
    x=lon,
    y=lat,
    style=style,
    direction=[np.rad2deg(np.arctan2(dn,de)), np.sqrt(dn**2 + de**2)],
    pen="1p",
    color="black",
)
#plot scale vector
fig.plot(
    x=-149,
    y=58.5,
    style='v0.25c+ea+a45',
    direction=[[0], [1]],
    pen='1p',
    color='black'
)
#plot scale label
fig.plot(
    x=-148.7,
    y=58.4,
    style='l0.25c+t"10 mm"',
    color='black'

)

# vector specifications structured as:
# [x_start, y_start, direction_degrees, length]
vector_2 = [-82, 40.5, 138, 2.5]
vector_3 = [-71.2, 45, -115.7, 4]
# Create a list of lists that include each vector information
vectors = [vector_2, vector_3]

# Plot vectors using the data parameter.
fig.plot(
    data=vectors,
    style=style,
    pen="1p",
    color="yellow",
)
fig.savefig('./Figures/Iniskin_GPS_Data.png')

