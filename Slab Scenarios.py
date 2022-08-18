import pygmt
import UsefulFunctions as uf
import pandas as pd

slab2path = 'Data/Slab Scenarios/Closest_slab2.txt'
slab2 = pd.read_csv(slab2path)
slab2 = slab2.round(decimals=2)
slab2 = slab2.drop('OBJECTID', axis=1)
slab2projected = pygmt.project(data=slab2,
                               center='-149.955/61.346',
                               azimuth=140)
print(slab2.info)
print(slab2projected.info)

title = r"Slab Scenarios Scenarios"
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
fig = pygmt.Figure()
# fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
fig.basemap(region='206.5/58/218/66.5+r', projection='M15c', frame=["af", f'WSne+t"{title}"'])
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1', land='gainsboro')  # draw coast over datawater='skyblue'

fig.plot(  # Plot seismic stations as triangles
    x=uf.ActiveBBs['lon'],
    y=uf.ActiveBBs['lat'],
    style='t+0.13c',
    color='white',
    pen='0.1p,black',
)

fig.plot(
    x=slab2projected[0],
    y=slab2projected[1],
    style='t+0.13c',
    color='black'
)
fig.plot(
    x=slab2projected[7],
    y=slab2projected[8],
    style='c+0.13c',
    color='green'
)

fig.savefig('Figures/Slab Scenarios/SlabScenarioMap.pdf')
