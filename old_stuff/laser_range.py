import ephem
import datetime
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
from ephem import degree
from math import sin, cos, sqrt, atan2, radians, acos, degrees
from best_position import *
import operator

print("Takes about 5 minutes")

filename = open("data/cleaned_tle.txt", "r").read().splitlines()

# start and finish time in year month day hour minute second
start = datetime(2020, 1, 10, 14, 0, 0)
finish = datetime(2020, 1, 10, 16, 0, 0)

name = "ISS (ZARYA)"

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

def lati_longi(l1, l2, time1, rounding=0, name="ISS (ZARYA)"):
    """
    Returns latitude and longitude of a satellite, can be rounded to 1, 2 or 5
    """
    tle_rec = ephem.readtle(name, l1, l2)
    tle_rec.compute(time1)
    lati = (tle_rec.sublat / degree)
    longi = (tle_rec.sublong / degree)
    if rounding != 0:
        lati = rounding * round(lati/rounding)
        longi = rounding * round(longi/rounding)
    return lati, longi

def calc_loc(dicti, filename):
    """
    Calculates the latitude and longitude that the satellites are above, keeps a
    dictionary of the latitude and longitudes that the most satellites are near
    """
    progress = 0
    highest_total = 0

    # Goes through all satellites
    for line in filename:
        cord_list = []
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
            lati, longi = lati_longi(l1, l2, i, 5)

            # Location of laser
            if (lati, longi) == (80.0, -15.0):
                satellite = twoline2rv(l1, l2, wgs72)
                time_list = (int(str(i)[0:4]), int(str(i)[5:7]), int(str(i)[8:10]),
                int(str(i)[11:13]), int(str(i)[14:16]), int(str(i)[17:19]))
                xyz, velocity = satellite.propagate(time_list[0], time_list[1],
                    time_list[2], time_list[3], time_list[4], time_list[5])
                cord_list.append(xyz)

        # Kilometers between the orbit of a satellite
        for i1 in cord_list:
            for j1 in cord_list:
                total = np.sqrt((i1[0] - j1[0])**2 + (i1[1] - j1[1])**2 + (i1[2] - j1[2])**2)
                if total > highest_total:
                    highest_total = total
                    best_i1 = i1
                    best_j1 = j1
        if progress % 30 == 0:
            percent_done = round(progress/len(filename)*100, 0)
            print("{} percent done" .format(percent_done), end="\r")

    # Calculates the angle that the laser should be able to reach
    # takes the maximum distance between two satellites while they are both in
    # the range of the laser. Then calculates the height of the satellites minus
    # the radius of the earth, finally calculates the angle of the laser
    b = np.sqrt((best_i1[0])**2 + (best_i1[1])**2 + (best_i1[2])**2) - 6371
    c = np.sqrt((best_j1[0])**2 + (best_j1[1])**2 + (best_j1[2])**2) - 6371
    angle_laser = degrees(acos((b**2 + c**2 - highest_total**2)/(2.0 * b * c)))
    print("Diameter of the sky: {}" .format(highest_total))
    print("The angle of the laser: {} degrees" .format(angle_laser))
    return cord_list

dicti = calc_loc(possible_coords(73, 37), filename)
