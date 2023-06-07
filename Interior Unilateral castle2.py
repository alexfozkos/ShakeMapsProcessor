import os
import pandas as pd
import UsefulFunctions as uf

MAG = 7.3
ID = 'INTERIORSCENARIOS'


def fixlons(df):
    df['lon'][df['lon'] > 180] -= 360  # convert lons past 180 to negative western lons
    return df

crst_hypocenters = pd.read_csv('Data/Interior Crustal/Crustal_Hypocenters.txt', delimiter='\t',
                               names=['lon', 'lat', 'depth', 'dip', 'strike', 'name'])

castle_2 = crst_hypocenters.iloc[-1]
for start in [2, 6]:
    p, LW = uf.createPlane(castle_2['lon'], castle_2['lat'], MAG, castle_2['depth'], castle_2['strike'], castle_2['dip'], 'ss')
    if start == 2:
        name = castle_2['name'] + '_NE'
    else:
        name = castle_2['name'] + '_SW'
    lat = p[start][1]
    lon = p[start][0]
    d = p[start][2]
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
    [[gmpe_QCF3_custom]]
        gmpes = active_crustal_nshmp2014,
        weights = 1.0,
        weights_large_dist = None
        dist_cutoff = nan
        site_gmpes = None
        weights_site_gmpes = None
[modeling]
    gmpe = gmpe_QCF3_custom
    mechanism = SS
    ipe = VirtualIPE
    gmice = WGRW12
    ccf = LB13''')

