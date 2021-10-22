# This file is for messing with the way activeBBs.txt is parsed, without screwing up UsefulFunctions.py

import UsefulFunctions as uf
import numpy as np
import re

eq = uf.Earthquake('Data/Iniskin_grid.xml')
print(eq.detection_time)
# Create an array from activeBBs.txt, specify data types and names for each column, delimit based on fixed char lengths
# ActiveBBs = np.genfromtxt('Data/activeBBs.txt',
#                           delimiter=[8, 9, 12, 8, 50],
#                           dtype=[('sta', 'U5'), ('lat', 'f8'), ('lon', 'f8'), ('elev', 'f8'), ('staname', 'U50')],
#                           autostrip=True,
#                           )
# for i in ActiveBBs['elev']:
#     print(i)
#
# print(ActiveBBs.shape)
