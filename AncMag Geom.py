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

MAGS = np.round(np.arange(5.0, 8.1, .1), decimals=1)
ID = 'ANCMAGSCENARIOS'


def fixlons(df):
    df['lon'][df['lon'] > 180] -= 360  # convert lons past 180 to negative western lons
    return df


anc_lat, anc_lon, anc_depth, anc_dip, anc_strike = 61.346, -149.955, 46.7, 62, 189
gmpe_name = 'ak018fcnsk91'
nshmp = 'subduction_interface_nshmp2014, subduction_slab_nshmp2014'
weights = '0.318025227722, 0.681974772278'
mech = 'is'
for mag in MAGS:
    p, LW = uf.createPlane(anc_lon+360, anc_lat, mag, anc_depth, anc_strike, anc_dip, mech)
    print(p)
    print(f'MAG: {mag}')
    # replace the decimal with an _ just incase weird file naming issues
    mag_string = str(mag).replace('.', '_')
    name = f'AncMag{mag_string}'
    path1 = f'Data/AncMag/Shakemap Folders/{name}'
    path2 = f'{path1}/current'
    if not os.path.exists(path1):
        os.mkdir(path1)
    if not os.path.exists(path2):
        os.mkdir(path2)
    with open(f'{path2}/event.xml', 'w') as f:  # event file
        f.write(f'<earthquake id="{ID}" netid="ak" network="Alaska Earthquake Center" lat="{anc_lat}" '
                f'lon="{anc_lon}" depth="{anc_depth}" mag="{mag}" time="2022-08-4T21:29:29Z" '
                f'locstring="{name}" event_type="SCENARIO"/>')
    with open(f'{path2}/rupture.json', 'w') as f:  # rupture file
        f.write(f'{{"metadata": {{"id": "{ID}", "netid": "ak", "network": "Alaska Earthquake Center", '
                f'"lat": {anc_lat}, "lon": {anc_lon}, "depth": {anc_depth}, "mag": {mag}, "time": "2022-03-28T21:29:29.000000Z", '
                f'"locstring": "{name}", "reference": "Fozkos 2022", "mech": "ALL", "rake": 0.0, '
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
    mechanism = NM
    ipe = VirtualIPE
    gmice = WGRW12
    ccf = LB13''')

    # add mechanism to the mechs.txt file (if not already) for rupture duration calculation in uf
    uf.update_mechstxt(name, mech)

#region map maker

# Create PyGMT map of scenarios

title = r"Anchorage Magnitude Scenarios"
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
fig = pygmt.Figure()
fig.basemap(region=f'{anc_lon+360-2}/{anc_lat-1}/{anc_lon+360+2}/{anc_lat+1}+r', projection='M15c', frame=["af", f'WSne+t"{title}"'])
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1', land='gainsboro')  # draw coast over datawater='skyblue'
ll = 1

starsize = 1.0
numsize = 0.45
# numsize2 = 0.25
planes = {}
for mag in MAGS:
    p, LW = uf.createPlane(anc_lon+360, anc_lat, mag, anc_depth, anc_strike, anc_dip, mech)
    if mag == 7.1:
        color = 'red'
        pt = 2
    else:
        color = 'black'
        pt = 1
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        transparency='50',
        pen=f'{pt}p,{color}'
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
    fig.text(
            text=str(mag),
            x=p[1][0],
            y=p[1][1],
            font=f"8p,Helvetica-Bold,{color}=0.45p,white"
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
fig.savefig('Figures/AncMag/AncMagScenarios.pdf')
#endregion map maker
