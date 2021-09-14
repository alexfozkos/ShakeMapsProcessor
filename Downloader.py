# downloads grid.xml from shakemaps url because I can't figure out how to
# download it otherwise

import requests

url1 = 'https://earthquake.alaska.edu/sites/all/web/shakemap/ak0216xu2rod/grid.xml'
url2 = 'https://earthquake.alaska.edu/sites/all/web/shakemap/ak0216xu2rod/stationlist.json'

response = requests.get(url1)
with open('grid.xml','wb') as file:
    file.write(response.content)

response = requests.get(url2)
with open('stations.json','wb') as file:
    file.write(response.content)
