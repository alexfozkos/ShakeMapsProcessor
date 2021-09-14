# Creates a scatter plot map of all data points in grid.xml and shades them according to PGA, using PyGMT

import numpy as np
import xml.etree.ElementTree as ET
import pygmt
import json

# read in the xml
tree = ET.parse('grid.xml')
root = tree.getroot()

# read in stations json
with open('stations.json') as file:
    stations = json.load(file)

station_coords = np.array([[]])

for feature in stations['features']:
    station_coords = np.append(station_coords, feature['geometry']['coordinates'])

station_coords = np.reshape(station_coords, (len(stations['features']), 2))


# grab event coords and grid size and grid bounds
elat = float(root[0].attrib['lat'])
elon = float(root[0].attrib['lon'])

nlat = int(root[1].attrib['nlat'])
nlon = int(root[1].attrib['nlon'])

lon_min = float(root[1].attrib['lon_min'])
lat_min = float(root[1].attrib['lat_min'])
lon_max = float(root[1].attrib['lon_max'])
lat_max = float(root[1].attrib['lat_max'])
gridBoundaries = [lon_min, lon_max, lat_min, lat_max]

# turn big data string into a nice array
gridDataArray = np.array(root[-1].text.replace('\n', ' ').split(' ')[1:-1], dtype=float)
gridDataArray = np.reshape(gridDataArray, (int(nlat * nlon), 9))

lats = gridDataArray[:, 1]
lons = gridDataArray[:, 0]
pga = gridDataArray[:, 3]

r_width = 15/nlon
r_height = 15/nlat

fig = pygmt.Figure()
fig.basemap(region=gridBoundaries, projection='M15c', frame=True)


pygmt.makecpt(
    transparency=50,
    cmap=['hot'],
    reverse=True,
    series=[0, np.max(pga)]
)

fig.plot(  # Plot seismic stations as triangles
    x=station_coords[:, 0],
    y=station_coords[:, 1],
    style='t+0.1c',
    color='white',
    pen='black',
)

fig.plot(  # plot pga data
    x=lons,
    y=lats,
    color=pga,
    cmap=True,
    style='r{}/{}'.format(r_width, r_height)  # Use .format to insert calculated values
)

# fig.plot(  # plot black dots at each data point
#     x=lons,
#     y=lats,
#     color='black',
#     style='p'
# )

fig.plot(  # plot epicenter
    x=elon,
    y=elat,
    style='a.2c',
    color='purple',
    pen='black'
)

fig.coast(shorelines=True, water='skyblue')  # draw coast over data
fig.colorbar(frame='af+l"PGA (%g)"')

fig.savefig('PyGMTMap.png')
