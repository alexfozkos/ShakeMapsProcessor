import UsefulFunctions as uf
from matplotlib import pyplot as plt

def testcreatePlane2(lon, lat, mag, depth, strike, dip, mech):
    import UsefulFunctions as uf
    from matplotlib import pyplot as plt

    points, LW = uf.createPlane2(lon, lat, mag, depth, strike, dip, mech)
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'silver', 'black']

    # plt.figure()
    for i in range(len(points)):
        plt.scatter(points[i][0], points[i][1], c=colors[i])

    plt.scatter(lon, lat, c='black', marker='*')
    # plt.savefig('Figures/misc/test_plane2.png')
    # plt.show()


lons = [-25, -25, 25, 25, 0, 20]
lats = [50, -50, 50, -50, 0, 0]
mag = 9.3
depth = 20
strikes = [0, 45, 60, 90, 145, 345]
dip = 9
mech = 'r'

plt.figure()
for i in range(len(lons)):
    testcreatePlane2(lons[i], lats[i], mag, depth, strikes[i], dip, mech)

plt.savefig('Figures/misc/test_plane2_mult.png')
plt.show()
