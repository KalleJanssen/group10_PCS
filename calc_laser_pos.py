"""
Calculates best place to place the laser and then the angle the laser should be
able to rotate (combines where_laser and laser_range)
"""

import ephem
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
import numpy as np
from ephem import degree
from math import sin, cos, sqrt, atan2, radians, acos, degrees
import operator

def hourly_it(start, finish):
    """
    Returns a list of all timepoints between a start and end date
    """
    while finish > start:
        start = start + timedelta(seconds=1)
        yield start

def decdeg2dms(dd):
    """
    Transforms decimal coordinates to dms format
    """
    is_positive = dd >= 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees1,minutes = divmod(minutes,60)
    degrees1 = degrees1 if is_positive else -degrees1
    return str(str(degrees1) + ':' + str(minutes) + ':' + str(seconds))

def height_sat(l1, l2, i, lati, longi):
    """
    Returns distance to a specific coordinate
    """
    laser = ephem.Observer()
    tle_rec = ephem.readtle("name", l1, l2)
    tle_rec.compute(i)
    laser.lon = decdeg2dms(longi)
    laser.lat = decdeg2dms(lati)
    laser.elevation = 0
    laser.date = i


    tle_rec = ephem.readtle("SAT", l1, l2)
    tle_rec.compute(laser)

    d = tle_rec.range / 1000

    return d

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


def possible_coords(rounding):
    """
    Makes a dictionary with all possible coordinate combinations, a rounding
    is added which decides in how many parts the longitude and latitude should
    be divided so that the laser can reach a bigger area. The different values
    should be 1, 2, 5 or 10
    """
    dicti = {}
    for longi in np.linspace(-180, 180, 360//rounding + 1):
        for lati in np.linspace(-90, 90, 180//rounding + 1):
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
            lati, longi = lati_longi(l1, l2, i, 5)
            if (lati, longi) not in listi:
                listi.append((lati, longi))

        # If above a coordinate a satellite was located add 1 to that coordinate
        for i in listi:
            dicti[i] += 1

        # Makes the progress bar
        if progress % 30 == 0:
            percent_done = int(progress/len(filename)*100)
            print("{} percent done first half" .format(percent_done), end="\r")
    # Coordinates with most satellites
    place = max(dicti.items(), key=operator.itemgetter(1))[0]

    return dicti, place


def calc_angle(dicti, filename, place):
    """
    Calculates the angle that the laser should be able to reach
    """
    progress = 0
    highest_total = 0
    maximum_distance = 0
    minimum_distance = 10000

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
            if (lati, longi) == place:
                satellite = twoline2rv(l1, l2, wgs72)
                time_list = (int(str(i)[0:4]), int(str(i)[5:7]), int(str(i)[8:10]),
                int(str(i)[11:13]), int(str(i)[14:16]), int(str(i)[17:19]))
                xyz, velocity = satellite.propagate(time_list[0], time_list[1],
                    time_list[2], time_list[3], time_list[4], time_list[5])
                cord_list.append(xyz)

                d = height_sat(l1, l2, i, lati, longi)

                if d > maximum_distance:
                    maximum_distance = d
                if d < minimum_distance:
                    minimum_distance = d

        # Kilometers between the orbit of a satellite
        for i1 in cord_list:
            for j1 in cord_list:
                total = np.sqrt((i1[0] - j1[0])**2 + (i1[1] - j1[1])**2 + (i1[2] - j1[2])**2)
                if total > highest_total:
                    highest_total = total
                    best_i1 = i1
                    best_j1 = j1
        if progress % 30 == 0:
            percent_done = int(progress/len(filename)*100)
            print("{} percent done second half" .format(percent_done), end="\r")

    # Calculates the angle that the laser should be able to reach
    # takes the maximum distance between two satellites while they are both in
    # the range of the laser. Then calculates the height of the satellites minus
    # the radius of the earth, finally calculates the angle of the laser
    b = np.sqrt((best_i1[0])**2 + (best_i1[1])**2 + (best_i1[2])**2) - 6371
    c = np.sqrt((best_j1[0])**2 + (best_j1[1])**2 + (best_j1[2])**2) - 6371
    angle_laser = degrees(acos((b**2 + c**2 - highest_total**2)/(2.0 * b * c)))
    return highest_total, angle_laser, minimum_distance, maximum_distance

if __name__ == '__main__':
    filename = open("data/output.txt", "r").read().splitlines()

    # start and finish time in year month day hour minute second
    start = datetime(2020, 1, 10, 14, 0, 0)
    finish = datetime(2020, 1, 10, 16, 0, 0)

    print("Takes about 5 minutes")

    dicti, place = calc_loc(possible_coords(5), filename)
    #
    print("Best place: {} (lati, longi) \nWith {} satellites" .format(place, dicti[place]))

    #place = (80, -15)
    h, a, mini, maxi = calc_angle(possible_coords(5), filename, place)

    print("Diameter of the sky: {} km" .format(round(h, 1)))
    print("The angle of the laser: {} degrees" .format(round(a, 1)))
    print("Closest satellite: {} km" .format(round(mini, 1)))
    print("Furthest satellite: {} km" .format(round(maxi, 1)))
