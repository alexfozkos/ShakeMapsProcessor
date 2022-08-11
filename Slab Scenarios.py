import pygmt
import UsefulFunctions as uf
import pandas as pd

slab2path = 'Data/Slab Scenarios/Closest_slab2.txt'
slab2 = pd.read_csv(slab2path)
slab2 = slab2.round(decimals=2)
slab2 = slab2.drop('OBJECTID', axis=1)
slab2projected = pygmt.project(data=slab2,
                               center='-149.955/61.346',
                               azimuth=140)
print(slab2.info)
print(slab2projected.info)
