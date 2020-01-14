import ephem
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from mpl_toolkits import mplot3d
import numpy as np
from ephem import degree
from math import sin, cos, sqrt, atan2, radians

def lati_long(line1, line2, name = "ISS (ZARYA)"):
    """
    Calculate latitude and longitude of a satellite at two different times and
    then calculates the distance between them in lower earth orbit
    """
    tle_rec = ephem.readtle(name, line1, line2)
    tle_rec.compute('2020/1/14 10:29:0')
    print("lati: {}, long: {}".format(tle_rec.sublat / degree, tle_rec.sublong / degree))

    tle_rec1 = ephem.readtle(name, line1, line2)
    tle_rec1.compute('2020/1/14 10:29:10')
    print("lati: {}, long: {}".format(tle_rec1.sublat / degree, tle_rec1.sublong / degree))

    satellite = twoline2rv(line1, line2, wgs72)
    i, velocity = satellite.propagate(2020, 1, 14, 10, 29, 0)
    j, velocity = satellite.propagate(2020, 1, 14, 10, 29, 10)
    total = np.sqrt((i[0] - j[0])**2 + (i[1] - j[1])**2 + (i[2] - j[2])**2)
    print("Distance in LEO: {} km" .format(total))
    return tle_rec, tle_rec1

def distance(tle_rec, tle_rec1):
    # radius of earth
    R = 6373.0

    lati = radians(tle_rec.sublat / degree)
    longi = radians(tle_rec.sublong / degree)
    lati1 = radians(tle_rec1.sublat / degree)
    longi1 = radians(tle_rec1.sublong / degree)

    dlon = longi1 - longi
    dlat = lati1 - lati

    a = sin(dlat / 2)**2 + cos(lati) * cos(lati1) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    print("Distance on ground: {} km" .format(distance))

line1 = "1  2435U 66087A   20006.84210147 -.00000023 +00000-0 +10264-3 0  9998"
line2 = "2  2435 100.9287 033.6566 0064427 070.0261 102.1624 12.56842164443355"

tle_rec, tle_rec1 = lati_long(line1, line2)
distance(tle_rec, tle_rec1)
