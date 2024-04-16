import os
import json
import matplotlib as mpl

mpl.rcParams["backend"] = "TkAgg"
import pandas as pd
import numpy as np
from numpy import sin, cos, pi
from matplotlib import pyplot as plt
import pygmt
import UsefulFunctions as uf

MAG = 7.8
ID = 'SLABSCENARIOS'

def fixlons(df):
    df['lon'][df['lon'] > 180] -= 360  # convert lons past 180 to negative western lons
    return df


dd_hypocenters = pd.read_csv('Data/Down Dip/sample_points_full.txt', delimiter=' ', comment='#')
print(dd_hypocenters.info)
# create rupture geometries
for index, row in dd_hypocenters.iterrows():
    p, [l, w] = uf.createPlane(row['lon'] + 360, row['lat'], MAG, row['depth'], row['strike'], row['dip'], row['mech'])
    print(f'INDEX: {index}')
    name = row['name']
    lat = row['lat']
    lon = row['lon']
    d = row['depth']
    path1 = f'Data/Down Dip/Shakemap Folders/{name}'
    path2 = f'{path1}/current'
    # define mechanism
    if row['mech'] == 'int':
        mech = 'RS'
    else:
        mech = 'NM'
    # define gmpes for model conf
    if index in [0, 1, 2, 3]:
        gmpe_name = 'deepslab'
        nshmp = 'subduction_slab_nshmp2014'
        weights = '1.0'
    elif index in [4, 5]:
        gmpe_name = 'ak018fcnsk91'
        nshmp = 'subduction_interface_nshmp2014, subduction_slab_nshmp2014'
        weights = '0.318025227722, 0.681974772278'
    elif index in [6, 7, 8, 9]:
        gmpe_name = 'interface'
        nshmp = 'subduction_interface_nshmp2014'
        weights = '1.0'
    else:
        gmpe_name = 'outerrise'
        nshmp = 'active_crustal_nshmp2014'
        weights = '1.0'

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
                f'"locstring": "{name}", "reference": "Fozkos 2022", "mech": "{mech}", "rake": 0.0, '
                f'"productcode": "{ID}"}}, "features": [{{"geometry": {{"coordinates": '
                f'[[[[{p[5][0]}, {p[5][1]}, {p[5][2]}], [{p[3][0]}, {p[3][1]}, {p[3][2]}], [{p[1][0]}, {p[1][1]}, {p[1][2]}], '
                f'[{p[7][0]}, {p[7][1]}, {p[7][2]}], [{p[5][0]}, {p[5][1]}, {p[5][2]}]]]], "type": "MultiPolygon"}}, '
                f'"properties": {{"rupture type": "rupture extent"}}, "type": "Feature"}}], '
                f'"type": "FeatureCollection"}}')

    with open(f'{path2}/model.conf', 'w') as f:  # model.conf
        f.write(f'''# This file (model_select.conf) is generated automatically by the 'select'
# coremod. It will be completely overwritten the next time select is run. To
# preserve these settings, or to modify them, copy this file to a file called
# 'model.conf' in the event's current directory. That event-specific
# model.conf will be used and model_select.conf will be ignored. (To avoid
# confusion, you should probably delete this comment section from your event-
# specific model.conf.)
[gmpe_sets]
    [[gmpe_{gmpe_name}_custom]]
        gmpes = {nshmp},
        weights = {weights},
        weights_large_dist = None
        dist_cutoff = nan
        site_gmpes = None
        weights_site_gmpes = None
[modeling]
    gmpe = gmpe_{gmpe_name}_custom
    mechanism = {mech}
    ipe = VirtualIPE
    gmice = WGRW12
    ccf = LB13''')

    # add mechanism to the mechs.txt file (if not already) for rupture duration calculation in uf
    uf.update_mechstxt(name, row['mech'])
# Create PyGMT map of scenarios

# #region map maker
# title = r"Subduction Cross Section Scenarios"
# coast_border = "a/0.25p,black"
# shorelines = "0.15p,black"
# fig = pygmt.Figure()
# # fig.basemap(region=[160, 240, 40, 75], projection='M15c', frame=True)
# fig.basemap(region='205.5/57.5/218/63.5+r', projection='M15c', frame=["af", f'WSne+t"{title}"'])
# fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1', land='gainsboro')  # draw coast over datawater='skyblue'
#
# fig.plot(  # Plot seismic stations as triangles
#     x=uf.ActiveBBs['lon'],
#     y=uf.ActiveBBs['lat'],
#     style='t+0.13c',
#     color='white',
#     pen='0.1p,black',
# )
#
# starsize = 1.0
# numsize = 0.45
# # numsize2 = 0.25
# planes = {}
# for index, row in dd_hypocenters.iterrows():
#     p, [l, w] = uf.createPlane(row['lon'], row['lat'], MAG, row['depth'], row['strike'], row['dip'], row['mech'])
#     planes[index] = p
#     fig.plot(
#         x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
#         y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
#         color='red',
#         transparency='50',
#         pen='1p,black'
#     )
#     # fig.plot(
#     #     x=p[0][0],
#     #     y=p[0][1],
#     #     style=f'a{starsize}c',
#     #     color='white',
#     #     pen='0.25p,red'
#     # )
#     # fig.plot(
#     #     x=p[0][0],
#     #     y=p[0][1],
#     #     style=f'l{numsize}c+t"{index + 1}"',
#     #     color='black'
#     # )
# for index, row in dd_hypocenters.iterrows():
#     fig.plot(
#         x=row['lon'],
#         y=row['lat'],
#         style=f'a{starsize}c',
#         color='white',
#         pen='0.25p,red'
#     )
#
#     if index < 9:
#         numsize2 = numsize
#     else:
#         numsize2 = numsize - 0.05
#
#     fig.plot(
#         x=row['lon'],
#         y=row['lat'],
#         style=f'l{numsize2}c+t"{index+1}"',
#         color='black'
#     )
# with open('Data/Southern Alaska Coast/Old Community Data.json') as json_file:
#     comm_dict = json.load(json_file)
# # plot communities
# for name, data in comm_dict.items():
#     fig.plot(
#         x=data['latlon'][1],
#         y=data['latlon'][0],
#         style='c0.08c',
#         color='black'
#     )
#     fig.text(
#         text=f'{name}',
#         x=data['latlon'][1] - 0.3,
#         y=data['latlon'][0] - 0.08,
#         font='6p,Helvetica,white',
#         fill='black',
#     )
# fig.savefig('Figures/Down Dip/ScenarioMap_pre.png', dpi=700)
# #endregion map maker
