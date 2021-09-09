# Creates a scatter plot map of all data points in grid.xml and shades them according to PGA, using PyGMT

import numpy as np
import xml.etree.ElementTree as ET
import pygmt


# read in the xml
tree = ET.parse('grid.xml')
root = tree.getroot()

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
gridDataArray = np.reshape(gridDataArray, (int(nlat*nlon), 9))

lats = gridDataArray[:, 1]
lons = gridDataArray[:, 0]
pga = gridDataArray[:, 3]
inc = [0.0464, 0.2506, 2.463, 3.44, 5.3, 10, 18.6, 34.6, 64.3]
limits = [0, 0.0464, 0.297, 2.76, 6.2, 11.5, 21.5, 40.1, 74.7, 139]

fig = pygmt.Figure()
fig.basemap(region=gridBoundaries, projection='M15c', frame=True)

pygmt.makecpt(
    transparency=80,  # This actually changes the transparency of the basemap, not the plotted points.
    cmap='hot',
    reverse=True,
    series=[0, np.max(pga)]
)

fig.plot(
    x=lons,
    y=lats,
    color=pga,
    cmap=True,
    style='c0.1c'
)

fig.coast(shorelines=True, water='skyblue')  # draw coast after makecpt so it isn't affected by transparency
fig.colorbar(frame='af+l"PGA (%g)"')

fig.show()
