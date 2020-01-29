"""
Calculates best place to place the laser
"""

import ephem
import datetime
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
from ephem import degree
from math import sin, cos, sqrt, atan2, radians
from best_position import *
import operator

filename = open("data/cleaned_tle.txt", "r").read().splitlines()

# start and finish time in year month day hour minute second
start = datetime(2020, 1, 10, 14, 0, 0)
finish = datetime(2020, 1, 10, 16, 0, 0)

print("Takes about 5 minutes")
print("Result should be (80.0, -15.0) (lati, longi) with 813 satellites")

name = "ISS (ZARYA)"

def myround(x, base):
    return base * round(x/base)

def possible_coords(n_long=361, n_lat=181):
    """
    Makes a dictionary with all possible coordinate combinations
    """
    dicti = {}
    for longi in np.linspace(-180, 180, n_long):
        for lati in np.linspace(-90, 90, n_lat):
            calc = (lati, longi)
            dicti[calc] = 0
    return dicti


def calc_loc(dicti, filename):
    """
    Calculates the latitude and longitude that the satellites are above, keeps a
    dictionary of the latitude and longitudes that the most satellites are near
    """
    progress = 0

    # Goes through all satellites
    for line in filename:
        progress += 1
        listi = []
        if line[0] == '1':
            l1 = line
            continue
        if line[0] == '2':
            l2 = line

        # Goes through all seconds of the given period and calculates the
        # coordinates for those seconds
        for i in hourly_it(start, finish):
            tle_rec = ephem.readtle(name, l1, l2)
            tle_rec.compute(i)
            # lati = round((tle_rec.sublat / degree), -1)
            # longi = round((tle_rec.sublong / degree), -1)
            lati = myround((tle_rec.sublat / degree), 5)
            longi = myround((tle_rec.sublong / degree), 5)
            if (lati, longi) not in listi:
                listi.append((lati, longi))

        # If above a coordinate a satellite was located add 1 to that coordinate
        for i in listi:
            dicti[i] += 1

        # Makes the progress bar
        if progress % 30 == 0:
            percent_done = round(progress/len(filename)*100, 0)
            print("{} percent done" .format(percent_done), end="\r")
    return dicti

dicti = calc_loc(possible_coords(73, 37), filename)

# Coordinates with most satellites
place = max(dicti.items(), key=operator.itemgetter(1))[0]
print("Best place: {} (lati, longi) \nWith {} satellites" .format(place, dicti[place]))