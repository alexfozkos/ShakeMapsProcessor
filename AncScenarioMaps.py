import matplotlib as mpl
mpl.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt
import numpy as np
import UsefulFunctions as uf
from impactutils.colors.cpalette import ColorPalette
import cartopy


anc_05 = uf.Earthquake('Data/AncScenarioGrids/Manual/grid05.xml')

shape = (anc_05.grid_spec['nlat'], anc_05.grid_spec['nlon'])
mmi_grid = anc_05.mmi.reshape(shape)
img_extent = [anc_05.lats.min(), anc_05.lats.max(), anc_05.lons.min(), anc_05.lons.max()]
X = anc_05.lons.reshape(shape)
Y = anc_05.lats.reshape(shape)
data = anc_05.pga.reshape(shape)

mmimap = ColorPalette.fromPreset('mmi')

geo_axes = plt.axes(projection=cartopy.crs.PlateCarree())
geo_axes.set_extent(img_extent, )
plt.imshow(mmi_grid, cmap=mmimap.cmap, transform=cartopy.crs.PlateCarree())
plt.contour(X, Y, data, transform=cartopy.crs.PlateCarree(), extent=img_extent)
plt.show()
