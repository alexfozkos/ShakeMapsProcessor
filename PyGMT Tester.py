# For playing around with pygmt and gmt
import pygmt
import UsefulFunctions as uf

gridBoundaries = [170, -128, 49, 73]
title = r"Test"
coast_border = "a/0.5p,gray"
shorelines = "0.5p,purple"
fig = pygmt.Figure()
fig.basemap(region='170/49/-128/73+r', projection='M15c', frame=["af", f'WSne+t"{title}"'])
fig.coast(shorelines=shorelines, borders=coast_border, water='skyblue')  # draw coast over data water='skyblue'

pygmt.makecpt(
    transparency=35,
    cmap=['seis'],
    reverse=True,
    series=[0, 60]  # np.max(p[2, :])
)
fig.plot(  # Plot seismic stations as triangles
    x=uf.ActiveBBs['lon'],
    y=uf.ActiveBBs['lat'],
    style='t+0.3c',
    color='white',
    pen='black',
)
fig.colorbar(frame='xafg20+l"Detection time (s)"')
fig.savefig('Figures/{}.png'.format(title))
