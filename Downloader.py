# downloads grid.xml from shakemaps url because I can't figure out how to
# download it otherwise

import requests

url = 'https://earthquake.alaska.edu/sites/all/web/shakemap/ak0216xu2rod/grid.xml'

response = requests.get(url)
with open('grid.xml','wb') as file:
    file.write(response.content)
