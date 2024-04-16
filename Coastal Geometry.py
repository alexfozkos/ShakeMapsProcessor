# This is a script to run the updated fault-plane function in UsefulFunctions, CreatePlane2, for the coastal scenarios.
# Its also to double check and make sure all my coastal scenarios are using the current warning time model numbers
# and manual ShakeMap config settings.
import os
import matplotlib as mpl
mpl.rcParams["backend"] = "TkAgg"
import pandas as pd
import numpy as np
import UsefulFunctions as uf
import pygmt


def fixlons(df):
    df['lon'][df['lon'] > 180] -= 360  # convert lons past 180 to negative western lons
    return df


alu_hypocenters = pd.read_csv('Data/Southern Alaska Coast/ALU_hypocenters.txt', delimiter='\t', names=['lon', 'lat', 'depth', 'dip', 'strike'])
alu_hypocenters = fixlons(alu_hypocenters)
qcf_hypocenters = pd.read_csv('Data/Southern Alaska Coast/QCF_hypocenters.txt', delimiter='\t', names=['lon', 'lat', 'depth', 'dip', 'strike'])
cse_hypocenters = pd.read_csv('Data/Southern Alaska Coast/CSE_hypocenters.txt', delimiter='\t', names=['lon', 'lat', 'depth', 'dip', 'strike'])

name_index = 1

# Aleutian Subduction Zone
for index, row in alu_hypocenters.iterrows():
    gmpe_name = 'AleutianSubductionZone'
    nshmp = 'subduction_interface_nshmp2014'
    mechanism = 'RS'
    p, LW = uf.createPlane2(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'int')
    name = f'SouthernCoast{name_index}'
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
    ccf = LB13
[extent]
    [[bounds]]
        # Coastal
        extent = -170.0, 51, -127.5, 66''')
    name_index += 1
    # add mechanism to the mechs.txt file (if not already) for rupture duration calculation in uf
    uf.update_mechstxt(name, 'int')

#region Create Shakemap Folders
# Chugach St. Elias Thrust
for index, row in cse_hypocenters.iterrows():
    gmpe_name = 'ChugachStElias'
    nshmp = 'active_crustal_nshmp2014'
    mechanism = 'RS'
    p, LW = uf.createPlane2(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'r')
    name = f'SouthernCoast{name_index}'
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
    ccf = LB13
[extent]
    [[bounds]]
        # Coastal
        extent = -170.0, 51, -127.5, 66''')
    name_index += 1
    # add mechanism to the mechs.txt file (if not already) for rupture duration calculation in uf
    uf.update_mechstxt(name, 'r')

# Queen Charlotte Fairweather Fault
for index, row in qcf_hypocenters.iterrows():
    gmpe_name = 'QueenCharlotteFairweather'
    nshmp = 'active_crustal_nshmp2014'
    mechanism = 'SS'
    p, LW = uf.createPlane2(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'ss')
    name = f'SouthernCoast{name_index}'
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
    ccf = LB13
[extent]
    [[bounds]]
        # Coastal
        extent = -170.0, 51, -127.5, 66''')
    name_index += 1
    # add mechanism to the mechs.txt file (if not already) for rupture duration calculation in uf
    uf.update_mechstxt(name, 'ss')

#endregion

#simple map test, not to be used as map figure generator
title = r"Coastal Test"
coast_border = "a/0.25p,black"
shorelines = "0.15p,black"
fig = pygmt.Figure()
fig.basemap(region=f'-170.0/51/-127.5/66+r', projection='M15c',
            frame=["af", f'WSne+t"{title}"'])
fig.coast(shorelines=shorelines, borders=coast_border, water='lightsteelblue1',
          land='gainsboro')  # draw coast over datawater='skyblue'
starsize = 0.5
numsize = 0.2
star_index = 1

for index, row in alu_hypocenters.iterrows():
    p, LW = uf.createPlane2(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'int')
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        color='red',
        transparency='75',
        pen='1p,gray'
    )

for index, row in alu_hypocenters.iterrows():
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'a{starsize}c',
        color='white',
        pen='0.25p,red'
    )
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'l{numsize}c+t"{star_index}"',
        color='black'
    )
    star_index += 1

planes = {}
for index, row in cse_hypocenters.iterrows():
    p, LW = uf.createPlane2(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'r')
    planes[index] = p
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        color='purple',
        transparency='75',
        pen='1p,gray'
    )

for index, row in cse_hypocenters.iterrows():
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'a{starsize}c',
        color='white',
        pen='0.25p,purple'
    )
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'l{numsize}c+t"{star_index}"',
        color='black'
    )
    star_index += 1

planes = {}
for index, row in qcf_hypocenters.iterrows():
    p, LW = uf.createPlane2(row['lon'], row['lat'], 8.3, row['depth'], row['strike'], row['dip'], 'ss')
    planes[index] = p
    fig.plot(
        x=[p[1][0], p[3][0], p[5][0], p[7][0], p[1][0]],
        y=[p[1][1], p[3][1], p[5][1], p[7][1], p[1][1]],
        color='green3',
        transparency='25',
        pen='1p,green3'
    )

for index, row in qcf_hypocenters.iterrows():
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'a{starsize}c',
        color='white',
        pen='0.25p,green3'
    )
    fig.plot(
        x=row['lon'],
        y=row['lat'],
        style=f'l{numsize}c+t"{star_index}"',
        color='black'
    )
    star_index += 1

fig.savefig('Figures/CoastalScenarios/cp2maptest.png')
