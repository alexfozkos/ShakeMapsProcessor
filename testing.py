import numpy as np
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET


tree = ET.parse('grid.xml')
root = tree.getroot()
elat = float(root[0].attrib['lat'])
elon = float(root[0].attrib['lon'])
nlat = int(root[1].attrib['nlat'])
nlon = int(root[1].attrib['nlon'])

gridDataArray = np.array(root[-1].text.replace('\n', ' ').split(' ')[1:-1], dtype=float)

gridDataArray = np.reshape(gridDataArray, (int(nlat*nlon), 9))
print(gridDataArray[:, 1])

xlon = gridDataArray[:, 0]
ylat = gridDataArray[:, 1]
pgaScale = gridDataArray[:, 3]

plt.pcolormesh()

# plt.scatter(xlon, ylat, s=pgaScale*.5)
plt.show()
