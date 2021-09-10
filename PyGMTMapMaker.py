# Creates a scatter plot map of all data points in grid.xml and shades them according to PGA, using PyGMT
import matplotlib.colors
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm

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
# I need to convert this matplotlib stuff to a PyGMT equivalent
#
# limits = np.array([[0, 0.0464, 0.297, 2.76, 6.2, 11.5, 21.5, 40.1, 74.7, 139]])
shakemap_colors = [(1, 1, 1),  # white
                   (228/255, 206/255, 235/255),  # Thistle
                   (141/255, 246/255, 246/255),  # Electric blue
                   (135/255, 248/255, 160/255),  # Light-green
                   (199/255, 255/255, 110/255),  # Inchworm
                   (255/255, 255/255, 65/255),  # Maximum yellow
                   (255/255, 176/255, 28/255),  # Honey yellow
                   (229/255, 78/255, 38/255),  # Flame
                   (189/255, 35/255, 21/255),  # International orange engineering
                   (141/255, 0/255, 0/255)  # Dark red
                   ]
# my_cmap = LinearSegmentedColormap.from_list('shakemap_colors', shakemap_colors)
# norm = matplotlib.colors.BoundaryNorm(limits[0], len(limits[0])-1)

fig = pygmt.Figure()
fig.basemap(region=gridBoundaries, projection='M15c', frame=True)

pygmt.makecpt(
    transparency=10,
    cmap=['hot'],
    reverse=True,
    series=[0, np.max(pga)],
)

fig.plot(
    x=lons,
    y=lats,
    color=pga,
    cmap=True,
    style='r0.0333/0.0333'  # Use .format to insert calculated values
                            # distance(mid lon, max lat), (mid lon, min lat) = k * distance(max lon, mid lat), (min lon,
                            # mid lat) -> dist2lons = k*dist2lat, width wil be 0.0333, height will be k*0.0333
)

fig.coast(shorelines=True, water='skyblue')  # draw coast over data
fig.colorbar(frame='af+l"PGA (%g)"')

fig.show()
