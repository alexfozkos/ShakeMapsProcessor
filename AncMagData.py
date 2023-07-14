import os
import UsefulFunctions as uf
import pandas as pd
import numpy as np




directory_in_str = 'Data/Down Dip/grids'
directory = os.fsencode(directory_in_str)

# anchorage lat lon
anc_lon = -149.8997
anc_lat = 61.2176

data = pd.DataFrame(columns=['name', 'mag', 'mmi', 'pga', 'wt_lower', 'wt_upper'])

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(f'''{file}
{filename}''')
    if filename.endswith(".xml"):
        eq = uf.Earthquake(directory_in_str+'/'+filename)
        eq_anc_index = uf.getNearestIndex(eq.lons, eq.lats, anc_lon, anc_lat)
        eq_name = eq.event['event_id']
        eq_mag = eq.event['magnitude']
        eq_mmi = eq.mmi[eq_anc_index]
        eq_pga = eq.pga[eq_anc_index]
        eq_wt_upper = eq.warning_times_upper
        eq_wt_lower = eq.warning_times_lower

    else:
        continue
