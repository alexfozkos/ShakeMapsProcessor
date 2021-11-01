import numpy as np
import UsefulFunctions as uf
import pygmt

n = 0.5
lonE = np.arange(-180, -129, n)
lonW = np.arange(171, 180-n, n)
lon = np.append(lonW, lonE)
m = 0.2
lat = np.arange(50, 72, m)

x, y = np.meshgrid(lon, lat)
p = np.vstack((x.ravel(), y.ravel()))
print(p.shape)
times = np.array([[]])
d = 100
for i in range(0, p.shape[1]):
    times = np.append(times, uf.calculateDetectionTime(p[0,i], p[1,i], d, 6.7))
    print(i)

p = np.vstack((p, times))
print(p.shape)
print(p[:, 0:5])

gridBoundaries = [170, -128, 49, 73]
title = r"Detection Times for Depth {}km".format(d)
fig = pygmt.Figure()
fig.basemap(region='170/49/-128/73+r', projection='M15c', frame=["af", f'WSne+t"{title}"'])
fig.coast(shorelines=True, borders='a', )  # draw coast over datawater='skyblue'

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

fig.plot(  # plot time data
    x=p[0, :],
    y=p[1, :],
    color=p[2, :],
    cmap=True,
    style='c0.1c'
)
fig.colorbar(frame='xafg20+l"Detection time (s)"')
fig.savefig('Figures/Detection Times depth {}km.png'.format(d))
