import numpy as np
import matplotlib.colors
from matplotlib import pyplot as plt
import matplotlib as mpl
import xml.etree.ElementTree as ET
from matplotlib.colors import LinearSegmentedColormap

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
pgaScale = gridDataArray[:, 3]
print(np.max(pgaScale))

shakemap_colors = [(1, 1, 1),  # white
                   (212/255, 201/255, 245/255),  # lavender
                   (97/255, 255/255, 230/255),  # light blue
                   # (215/255, 234/255, 92/255),  # yellow-green
                   (1, 239/255, 0),  # yellow
                   # (1, 168, 0),  # orange
                   (184/255, 0, 0),  # red
                   (101/255, 0, 0)  # dark red
                   ]
my_cmap = LinearSegmentedColormap.from_list('shakemap_colors', shakemap_colors)

plt.plot(elon, elat, 'k*')
plt.scatter(xlon, ylat, s=.3, c=pgaScale, cmap=my_cmap, norm=matplotlib.colors.LogNorm())
plt.xlabel('Longitude (deg)')
plt.ylabel('Latitude (deg)')
cbar = plt.colorbar(label='PGA (%g)', extend='max', ticks=[0, 0.0464, 0.297, 2.76, 6.2, 11.5, 21.5, 40.1, 74.7, 139])
cbar.set_ticklabels(['0', '0.0464', '0.297', '2.76', '6.2', '11.5', '21.5', '40.1', '74.7', '139'])
# plt.clim(0.001, 139)
plt.savefig('scattermap.png')
