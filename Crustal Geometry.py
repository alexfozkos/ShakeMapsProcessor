import os
import json
import matplotlib as mpl
import geopandas as gpd
mpl.rcParams["backend"] = "TkAgg"
import pandas as pd
import numpy as np
from numpy import sin, cos, pi
from matplotlib import pyplot as plt
import pygmt
import UsefulFunctions as uf

MAG = 7.3
ID = 'INTERIORSCENARIOS'


def km2lat(d):
    return d / 110.574


def km2lon(d, lat):
    return d / (111.320 * cos(np.deg2rad(lat)))


def fixlons(df):
    df['lon'][df['lon'] > 180] -= 360  # convert lons past 180 to negative western lons
    return df


crst_hypocenters = pd.read_csv('Data/Interior Crustal/Crustal_Hypocenters.txt', delimiter='\t',
                               names=['lon', 'lat', 'depth', 'dip', 'strike', 'name'])
print(crst_hypocenters.info)
p_list = []
# create rupture geometries
for index, row in crst_hypocenters.iterrows():
    p, LW = uf.createPlane2(row['lon']-360, row['lat'], MAG, row['depth'], row['strike'], row['dip'], 'ss')
    p_list.append(p)
    print(f'INDEX: {index}')
    name = f'Crustal{index+1}'
    lat = row['lat']
    lon = row['lon'] - 360
    d = row['depth']
    path1 = f'Data/Interior Crustal/Shakemap Folders/{name}'
    path2 = f'{path1}/current'
    if not os.path.exists(path1):
        os.mkdir(path1)
    if not os.path.exists(path2):
        os.mkdir(path2)
    with open(f'{path2}/event.xml', 'w') as f:  # event file
        f.write(f'<earthquake id="{ID}" netid="ak" network="Alaska Earthquake Center" lat="{lat}" '
                f'lon="{lon}" depth="{d}" mag="{MAG}" time="2022-08-4T21:29:29Z" '
                f'locstring="{name}" event_type="SCENARIO"/>')
    with open(f'{path2}/rupture.json', 'w') as f:  # rupture file
        f.write(f'{{"metadata": {{"id": "{ID}", "netid": "ak", "network": "Alaska Earthquake Center", '
                f'"lat": {lat}, "lon": {lon}, "depth": {d}, "mag": {MAG}, "time": "2022-03-28T21:29:29.000000Z", '
                f'"locstring": "{name}", "reference": "Fozkos 2022", "mech": "SS", "rake": 0.0, '
                f'"productcode": "{ID}"}}, "features": [{{"geometry": {{"coordinates": '
                f'[[[[{p[5][0]}, {p[5][1]}, {p[5][2]}], [{p[3][0]}, {p[3][1]}, {p[3][2]}], [{p[1][0]}, {p[1][1]}, {p[1][2]}], '
                f'[{p[7][0]}, {p[7][1]}, {p[7][2]}], [{p[5][0]}, {p[5][1]}, {p[5][2]}]]]], "type": "MultiPolygon"}}, '
                f'"properties": {{"rupture type": "rupture extent"}}, "type": "Feature"}}], '
                f'"type": "FeatureCollection"}}')
    with open(f'{path2}/model.conf', 'w') as f:
        f.write('''# This file (model_select.conf) is generated automatically by the 'select'
# coremod. It will be completely overwritten the next time select is run. To
# preserve these settings, or to modify them, copy this file to a file called
# 'model.conf' in the event's current directory. That event-specific
# model.conf will be used and model_select.conf will be ignored. (To avoid
# confusion, you should probably delete this comment section from your event-
# specific model.conf.)
[gmpe_sets]
    [[gmpe_Crustal_custom]]
        gmpes = active_crustal_nshmp2014,
        weights = 1.0,
        weights_large_dist = None
        dist_cutoff = nan
        site_gmpes = None
        weights_site_gmpes = None
[modeling]
    gmpe = gmpe_Crustal_custom
    mechanism = SS
    ipe = VirtualIPE
    gmice = WGRW12
    ccf = LB13
[extent]
    [[bounds]]
        # Crustal
        extent = -153.5, 60.5, -142, 66.5''')

    uf.update_mechstxt(name, 'ss')

#region map maker

# Create PyGMT map of scenarios

# gdf = gpd.read_file('Data/faults/mp141/shapefiles/mp141-qflt-line-alaska.shp')
# # gdf = gdf.drop(['CODE', 'NUM', 'AGE', 'ACODE', 'SLIPRATE', 'SLIPCODE', 'SLIPSENSE', 'DIPDIRECTI', 'FCODE', 'FTYPE', 'SecondaryS'], axis=1)
# searchfor = 'Denali fault|Castle Mountain fault|Northern Foothills fold and thrust belt|seismic zone|Tintina'
# linestrings = [geom for geom in gdf[gdf['NAME'].str.contains(searchfor, regex=True)].geometry]
# linestrings = [geom for geom in gdf.geometry]

# all_data = []
# all_data.append(gdf[gdf['NAME'].str.contains(searchfor, regex=True)])
# gdf.plot()
# plt.show()

title = r"Interior Crustal Scenarios"
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
fig = pygmt.Figure()
# fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
fig.basemap(region='206.5/60.5/218/66.5+r', projection='M15c', frame=["af", f'WSne+t"{title}"'])
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1', land='gainsboro')  # draw coast over datawater='skyblue'
ll = 1

fig.plot(  # Plot seismic stations as triangles
    x=uf.ActiveBBs['lon'],
    y=uf.ActiveBBs['lat'],
    style='t+0.13c',
    color='white',
    pen='0.1p,black',
)



starsize = 1.0
numsize = 0.45
# numsize2 = 0.25
for p in p_list:
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        color='black',
        transparency='25',
        pen='2p,black'
    )
    # fig.plot(
    #     x=p[0][0],
    #     y=p[0][1],
    #     style=f'a{starsize}c',
    #     color='white',
    #     pen='0.25p,red'
    # )
    # fig.plot(
    #     x=p[0][0],
    #     y=p[0][1],
    #     style=f'l{numsize}c+t"{index + 1}"',
    #     color='black'
    # )
for index, row in crst_hypocenters.iterrows():
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'a{starsize}c',
        color='white',
        pen='0.25p,red'
    )

    if index < 9:
        numsize2 = numsize
    else:
        numsize2 = numsize - 0.05

    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'l{numsize2}c+t"{index+1}"',
        color='black'
    )

with open('Data/Southern Alaska Coast/Old Community Data.json') as json_file:
    comm_dict = json.load(json_file)
# plot communities
for name, data in comm_dict.items():
    fig.plot(
        x=data['latlon'][1],
        y=data['latlon'][0],
        style='c0.08c',
        color='black'
    )
    # fig.plot(
    #     x=data['latlon'][1],
    #     y=data['latlon'][0] + 0.1,
    #     style=f'l0.25c+t"{name}"',
    #     color='black'
    # )
    fig.text(
        text=name,
        x=data['latlon'][1],
        y=data['latlon'][0] + 0.1,
        font="10p,Helvetica-Bold,black"
    )
fig.savefig('Figures/Interior Crustal/CrustalMapTest.pdf')
#endregion map maker
