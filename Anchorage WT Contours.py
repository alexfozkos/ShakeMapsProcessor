import UsefulFunctions as uf
import numpy as np
import pandas as pd
import pygmt

anc = uf.Earthquake('Data/AncScenarioGrids/Anc2018.xml')

cmap = [(255, 255, 255),
        (191, 204, 255),
        (160, 230, 255),
        (128, 255, 255),
        (122, 255, 147),
        (255, 255, 0),
        (255, 200, 0),
        (255, 145, 0),
        (255, 0, 0),
        (200, 0, 0)]
mmi_rng = range(1, 11)
cpt = pygmt.makecpt(cmap="Data/mmi.cpt", series=[1, 11])
title = r"Alaska Southern Coast Scenarios"
bounds = '206/59/215/63.5+r'
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
frame = ["af", f'WSne+t"{title}"']
relief = pygmt.datasets.load_earth_relief(resolution="03s", region=[206, 215, 59, 63.5], registration='gridline')
fig = pygmt.Figure()
# fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
fig.basemap(region=bounds, projection='M15c', frame=frame)
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1',
          land='gainsboro')  # draw coast over datawater='skyblue'
fig.grdimage(grid=relief, projection='M15c', region=bounds, cmap='gray')
# fig.plot(x=anc.lons.flat,
#          y=anc.lats.flat,
#          color=anc.mmi.flat,
#          cmap='Data/mmi.cpt',
#          style='s.02c',
#          transparency=5
#          )


fig.coast(shorelines=True, water='skyblue')  # draw coast over data
fig.colorbar(frame='af+l"MMI"')
fig.show()
