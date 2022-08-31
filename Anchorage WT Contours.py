import UsefulFunctions as uf
import numpy as np
import pandas as pd
import pygmt

anc = uf.Earthquake('Data/AncScenarioGrids/Anc2018.xml')

title = r"Alaska Southern Coast Scenarios"
bounds = '206/59/215/63.5+r'
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
frame = ["af", f'WSne+t"{title}"']
fig = pygmt.Figure()
# fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
fig.basemap(region=bounds, projection='M15c', frame=frame)
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1', land='gainsboro')  # draw coast over datawater='skyblue'

