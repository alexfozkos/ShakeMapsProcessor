# This is a script to run the updated fault-plane function in UsefulFunctions, CreatePlane2, for the coastal scenarios.
# Its also to double check and make sure all my coastal scenarios are using the current warning time model numbers
# and manual ShakeMap config settings.
import os
import json
import matplotlib as mpl
mpl.rcParams["backend"] = "TkAgg"
import pandas as pd
import numpy as np
from numpy import sin, cos, pi
from matplotlib import pyplot as plt
import UsefulFunctions as uf


def fixlons(df):
    df['lon'][df['lon'] > 180] -= 360  # convert lons past 180 to negative western lons
    return df


def km2lat(d):
    return d/110.574


def km2lon(d, lat):
    return d/(111.320*cos(np.deg2rad(lat)))



alu_hypocenters = pd.read_csv('Data/Southern Alaska Coast/ALU_hypocenters.txt', delimiter='\t', names=['lon', 'lat', 'depth', 'dip', 'strike'])
alu_hypocenters = fixlons(alu_hypocenters)
qcf_hypocenters = pd.read_csv('Data/Southern Alaska Coast/QCF_hypocenters.txt', delimiter='\t', names=['lon', 'lat', 'depth', 'dip', 'strike'])
cse_hypocenters = pd.read_csv('Data/Southern Alaska Coast/CSE_hypocenters.txt', delimiter='\t', names=['lon', 'lat', 'depth', 'dip', 'strike'])


#region Create Shakemap Folders
# Chugach St. Elias Thrust
for index, row in cse_hypocenters.iterrows():
    gmpe_name = 'ChugachStElias'
    nshmp = 'active_crustal_nshmp2014'
    mechanism = 'RS'
    p, LW = uf.createPlane2(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'r')
    name = f'CSE{index}'
    lat = row['lat']
    lon = row['lon']
    d = row['depth']
    path1 = f'Data/Southern Alaska Coast/Shakemap Folders/{name}'
    path2 = f'{path1}/current'
    if not os.path.exists(path1):
        os.mkdir(path1)
    if not os.path.exists(path2):
        os.mkdir(path2)
    with open(f'{path2}/event.xml', 'w') as f:  # event file
        f.write(f'<earthquake id="COASTALSCENARIOS" netid="ak" network="Alaska Earthquake Center" lat="{lat}" '
                f'lon="{lon}" depth="{d}" mag="8.3" time="2022-03-28T21:29:29Z" '
                f'locstring="Chugach St. Elias Thrust" event_type="SCENARIO"/>')
    with open(f'{path2}/rupture.json', 'w') as f:  # rupture file
        f.write(f'{{"metadata": {{"id": "COASTALSCENARIOS", "netid": "ak", "network": "Alaska Earthquake Center", '
                f'"lat": {lat}, "lon": {lon}, "depth": {d}, "mag": 8.3, "time": "2022-03-28T21:29:29.000000Z", '
                f'"locstring": "Chugach St. Elias Thrust", "reference": "Fozkos 2022", "mech": "{mechanism}", "rake": 0.0, '
                f'"productcode": "COASTALSCENARIOS"}}, "features": [{{"geometry": {{"coordinates": '
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
        weights = 1.0,
        weights_large_dist = None
        dist_cutoff = nan
        site_gmpes = None
        weights_site_gmpes = None
[modeling]
    gmpe = gmpe_{gmpe_name}_custom
    mechanism = {mechanism}
    ipe = VirtualIPE
    gmice = WGRW12
    ccf = LB13''')

# Aleutian Subduction Zone
for index, row in alu_hypocenters.iterrows():
    gmpe_name = 'AleutianSubductionZone'
    nshmp = 'subduction_interface_nshmp2014'
    mechanism = 'RS'
    p, LW = uf.createPlane2(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'int')
    name = f'ALU{index}'
    lat = row['lat']
    lon = row['lon']
    d = row['depth']
    path1 = f'Data/Southern Alaska Coast/Shakemap Folders/{name}'
    path2 = f'{path1}/current'
    if not os.path.exists(path1):
        os.mkdir(path1)
    if not os.path.exists(path2):
        os.mkdir(path2)
    with open(f'{path2}/event.xml', 'w') as f:  # event file
        f.write(f'<earthquake id="COASTALSCENARIOS" netid="ak" network="Alaska Earthquake Center" lat="{lat}" '
                f'lon="{lon}" depth="{d}" mag="8.3" time="2022-03-28T21:29:29Z" '
                f'locstring="Aleutian Subduction Zone" event_type="SCENARIO"/>')
    with open(f'{path2}/rupture.json', 'w') as f:  # rupture file
        f.write(f'{{"metadata": {{"id": "COASTALSCENARIOS", "netid": "ak", "network": "Alaska Earthquake Center", '
                f'"lat": {lat}, "lon": {lon}, "depth": {d}, "mag": 8.3, "time": "2022-03-28T21:29:29.000000Z", '
                f'"locstring": "Aleutian Subduction Zone", "reference": "Fozkos 2022", "mech": "{mechanism}", "rake": 0.0, '
                f'"productcode": "COASTALSCENARIOS"}}, "features": [{{"geometry": {{"coordinates": '
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
        weights = 1.0,
        weights_large_dist = None
        dist_cutoff = nan
        site_gmpes = None
        weights_site_gmpes = None
[modeling]
    gmpe = gmpe_{gmpe_name}_custom
    mechanism = {mechanism}
    ipe = VirtualIPE
    gmice = WGRW12
    ccf = LB13''')

# Queen Charlotte Fairweather Fault
for index, row in qcf_hypocenters.iterrows():
    gmpe_name = 'QueenCharlotteFairweather'
    nshmp = 'active_crustal_nshmp2014'
    mechanism = 'SS'
    p, LW = uf.createPlane2(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'ss')
    name = f'QCF{index}'
    lat = row['lat']
    lon = row['lon']
    d = row['depth']
    path1 = f'Data/Southern Alaska Coast/Shakemap Folders/{name}'
    path2 = f'{path1}/current'
    if not os.path.exists(path1):
        os.mkdir(path1)
    if not os.path.exists(path2):
        os.mkdir(path2)
    with open(f'{path2}/event.xml', 'w') as f:  # event file
        f.write(f'<earthquake id="COASTALSCENARIOS" netid="ak" network="Alaska Earthquake Center" lat="{lat}" '
                f'lon="{lon}" depth="{d}" mag="8.3" time="2022-03-28T21:29:29Z" '
                f'locstring="Queen Charlotte Fairweather Fault" event_type="SCENARIO"/>')
    with open(f'{path2}/rupture.json', 'w') as f:  # rupture file
        f.write(f'{{"metadata": {{"id": "COASTALSCENARIOS", "netid": "ak", "network": "Alaska Earthquake Center", '
                f'"lat": {lat}, "lon": {lon}, "depth": {d}, "mag": 8.3, "time": "2022-03-28T21:29:29.000000Z", '
                f'"locstring": "Queen Charlotte Fairweather Fault", "reference": "Fozkos 2022", "mech": "{mechanism}", "rake": 0.0, '
                f'"productcode": "COASTALSCENARIOS"}}, "features": [{{"geometry": {{"coordinates": '
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
        weights = 1.0,
        weights_large_dist = None
        dist_cutoff = nan
        site_gmpes = None
        weights_site_gmpes = None
[modeling]
    gmpe = gmpe_{gmpe_name}_custom
    mechanism = {mechanism}
    ipe = VirtualIPE
    gmice = WGRW12
    ccf = LB13''')
#endregion

