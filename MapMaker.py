import numpy as np
import matplotlib.colors
from matplotlib import pyplot as plt
import matplotlib as mpl
import xml.etree.ElementTree as ET
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm, ListedColormap

tree = ET.parse('grid.xml')
root = tree.getroot()
elat = float(root[0].attrib['lat'])
elon = float(root[0].attrib['lon'])
nlat = int(root[1].attrib['nlat'])
nlon = int(root[1].attrib['nlon'])

gridDataArray = np.array(root[-1].text.replace('\n', ' ').split(' ')[1:-1], dtype=float)

gridDataArray = np.reshape(gridDataArray, (int(nlat*nlon), 9))
# print(gridDataArray[:, 1])

xlon = gridDataArray[:, 0]
ylat = gridDataArray[:, 1]
pga = gridDataArray[:, 3]
# print(np.max(pgaScale))
cbounds = np.array([[0, 0.0464, 0.297, 2.76, 6.2, 11.5, 21.5, 40.1, 74.7, 139]])

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
my_cmap = ListedColormap(shakemap_colors)
norm = matplotlib.colors.BoundaryNorm(cbounds[0], len(cbounds[0])-1)  # normalizes colors to the boundaries

plt.plot(elon, elat, 'k*')
plt.scatter(xlon, ylat, s=.3, c=pga, cmap=my_cmap, norm=norm)
plt.xlabel('Longitude (deg)')
plt.ylabel('Latitude (deg)')
cbar = plt.colorbar(label='PGA (%g)', extend='max', ticks=cbounds[0])
cbar.set_ticklabels(['0', '0.0464', '0.297', '2.76', '6.2', '11.5', '21.5', '40.1', '74.7', '139'])
plt.clim(0, 139)
plt.savefig('scattermap.png')
