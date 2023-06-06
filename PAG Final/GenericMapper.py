# Script to create a ground motion intensity map with warning time contours overlayed, including some communities
# must be run with a grid.xml file path as an argument
# GMT errors occur on machines that aren't my personal pc, errors say missing libraries?
import sys
import UsefulFunctions_PAG as uf  # this contains my custom earthquake class for parsing ShakeMap4 grid.xml files
import pygmt

# path to the grid.xml file
file_path = sys.argv[1]
# file_path = 'Anc2018.xml'
# parse the xml file
eq = uf.Earthquake(file_path)

# make a colormap with the ShakeMap colors for ground motion
cpt = pygmt.makecpt(cmap="mmi.cpt", series=[1, 11])
# define some map parameters
bounds = f'{eq.grid_spec["lon_min"]}/{eq.grid_spec["lat_min"]}/{eq.grid_spec["lon_max"]}/{eq.grid_spec["lat_max"]}+r'
coast_border = "a/0.25p,black"
shorelines = "0.1p,black"
# symbol size settings
starsize = 1.0
numsize = 0.35
ruptpen = 0.5
starpen = 0.75
fig = pygmt.Figure()
fig.basemap(region=bounds, projection='M15c')
fig.coast(shorelines=shorelines, borders=coast_border, water='skyblue2',
          land='gainsboro')
# plot the ground motion intensities across the map
fig.plot(x=eq.lons.flat,
         y=eq.lats.flat,
         color=eq.mmi.flat,
         cmap=True,
         style='r.024/.047c',
         )

fig.coast(shorelines=shorelines, water='skyblue2', map_scale='n0.5/0.05+w200+f+u')  # redraw coast and sea over data
fig.plot(  # Plot seismic stations as triangles
    x=uf.ActiveBBs['lon'],
    y=uf.ActiveBBs['lat'],
    style='t+0.18c',
    color='white',
    pen='0.1p,black',
)
# plot the epicenter as a star
fig.plot(x=eq.event['lon'],
         y=eq.event['lat'],
         style=f'a{starsize}c',
         color='white',
         pen=f'{starpen}p,red')
# plot warning time contours with 10 second intervals
fig.contour(x=eq.lons.flat,
            y=eq.lats.flat,
            z=eq.warning_times_s.flat,
            projection='M15c',
            region=bounds,
            levels=10,
            annotation=10,
            pen='1,black')
# plot communities
for comm, v in uf.community_dict.items():
    lat = v['latlon'][0]
    lon = v['latlon'][1]
    name = comm
    # plot a dot at the city location
    fig.plot(
        x=lon,
        y=lat,
        style='c0.08c',
        color='black'
    )
    # plot the name of the city slightly above
    corner = 'BR'
    adjust = 0.025
    fig.text(
        x=lon,
        y=lat + adjust,
        text=name,
        font='10p,Helvetica-Narrow-Bold,black,=0.45p,white',
        justify=corner
    )

fig.colorbar(position='JBC', frame='x+lMMI')
fig.savefig('Map.png', dpi=700)
