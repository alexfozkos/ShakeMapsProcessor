import UsefulFunctions as uf
import numpy as np
import pandas as pd
import pygmt

anc = uf.Earthquake('Data/AncScenarioGrids/Anc2018.xml')
cities = [(-150.1066, 62.3209, 'Talkeetna'),
          (-149.4411, 61.5809, 'Wasilla'),
          (-149.1146, 61.5994, 'Palmer'),
          (-149.8997, 61.2176, 'Anchorage'),
          (-151.0572, 60.4864, 'Soldotna'),
          (-151.5299, 59.6481, 'Homer'),
          (-149.4421, 60.1048, 'Seward'),
          (-146.3499, 61.1309, 'Valdez'),
          (-145.5340, 62.1081, 'Glennallen')]

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
cpt = pygmt.makecpt(cmap="Data/mmi_short.cpt", series=[3, 8])
title = r"Anchorage 2018 Estimated WT"
bounds = '206/59/215/63.5+r'
coast_border = "a/0.25p,black"
shorelines = "0.1p,black"
# frame = ["a", f'WSne+t"{title}"']
# relief = pygmt.datasets.load_earth_relief(resolution="03s", region=[206, 215, 59, 63.5], registration='gridline')
fig = pygmt.Figure()
# fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
fig.basemap(region=bounds, projection='M15c', frame=False)
fig.coast(shorelines=shorelines, borders=coast_border, water='skyblue2',
          land='gainsboro', frame=False)  # draw coast over datawater='skyblue'
# fig.grdimage(grid=relief, projection='M15c', region=bounds, cmap='gray')
fig.plot(x=anc.lons.flat,
         y=anc.lats.flat,
         color=anc.mmi.flat,
         cmap=True,
         style='r.018/.032c',
         )

starsize=.6
fig.coast(shorelines=shorelines, water='skyblue2', frame=False)  # draw coast over data
# fig.plot(  # Plot seismic stations as triangles
#     x=uf.ActiveBBs['lon'],
#     y=uf.ActiveBBs['lat'],
#     style='t+0.13c',
#     color='white',
#     pen='0.1p,black',
# )
fig.plot(x=anc.event['lon'],
         y=anc.event['lat'],
         style=f'a{starsize}c',
         color='white',
         pen='0.25p,red')
# fig.contour(x=anc.lons.flat,
#             y=anc.lats.flat,
#             z=anc.mmi.flat,
#             projection='M15c',
#             region=bounds,
#             levels=1,
#             annotation=1,
#             pen='red')
for city in cities:
    fig.plot(x=city[0],
             y=city[1],
             style='c0.08c',
             pen='0.02c,black',
             color='white')
fig.contour(x=anc.lons.flat,
            y=anc.lats.flat,
            z=anc.warning_times_s.flat,
            projection='M15c',
            region=bounds,
            levels=10,
            annotation=10,
            pen='0.04c,black')
fig.colorbar(position="JMR+o1c/0c+w7c/0.5c+mc")
fig.show()
fig.savefig('Figures/ancwtcolor.pdf', dpi=300)
fig.savefig('Figures/ancwtcolor.png')
