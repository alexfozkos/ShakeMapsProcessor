import UsefulFunctions as uf
import pandas as pd
import numpy as np

eq = uf.Earthquake('01192024.xml')
lats = eq.lats.flatten()
lons = eq.lons.flatten()
mmi = eq.mmi.flatten()
print(lats)

df = pd.DataFrame({'lat': lats, 'lon': lons, 'mmi': mmi})
print(df)
df.to_csv('mmi.csv', index=False)
