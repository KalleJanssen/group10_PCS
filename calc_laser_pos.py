import ephem
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
import numpy as np
from ephem import degree
from math import sin, cos, sqrt, atan2, radians, acos, degrees
import operator

"""
------------------------------------------------------------------------------------
The functions in this file are being used to calculate the best position to place
the laser and the angle the laser should be able to rotate to determine its range
------------------------------------------------------------------------------------
"""

def hourly_it(start, finish):
    """
    This function yields a list of all timepoints
    between a start and end date
    :param start: start timepoint
    :param finish: begin timepoint
    :return: list of all timepoints between a start and end date
    """

    while finish > start:
        start = start + timedelta(seconds=1)
        yield start

def decdeg2dms(dd):
    """
    This function transforms decimal coordinates to DMS format
    :param dd: decimal coordinates
    :return: DMS formatted coordinates
    """

    # convert coordinates to dms format
    is_positive = dd >= 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees1,minutes = divmod(minutes,60)
    degrees1 = degrees1 if is_positive else -degrees1

    return str(str(degrees1) + ':' + str(minutes) + ':' + str(seconds))

def height_sat(l1, l2, i, lati, longi):
    """
    This function calculates the distance
    of a satellite to a specific coordinate
    :param l1: TLE line 1
    :param l2: TLE line 2
    :param i: date in datetime format
    :param lati: latitude of coordinate
    :param longi: longitude of coordinate
    :return: distance between satellite and coordinate
    """

    # calculate distance between object on earth
    # and satellite in meters
    laser = ephem.Observer()
    tle_rec = ephem.readtle("name", l1, l2)
    tle_rec.compute(i)
    laser.lon = decdeg2dms(longi)
    laser.lat = decdeg2dms(lati)
    laser.elevation = 0
    laser.date = i
    tle_rec = ephem.readtle("SAT", l1, l2)
    tle_rec.compute(laser)

    # convert to kilometers
    d = tle_rec.range / 1000

    return d

def lati_longi(l1, l2, time1, rounding=0, name="ISS (ZARYA)"):
    """
    This function calculates the latitude and longitude of a satellite,
    which can be rounded to 1, 2 or 5
    :param l1: TLE line 1
    :param l2: TLE line 2
    :param time1: timestamp in datetime format
    :param rounding: rounding factor
    :param name: can be ignored
    :return: latitude and longitude of satellite
    """

    # calculate latitude and longitude using Ephem
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
    :param rounding: rounding factor
    :return: dictionary with all possible coordinate combinations
    """

    # create the dictionary with all possible coordinate combinations
    dicti = {}
    for longi in np.linspace(-180, 180, 360//rounding + 1):
        for lati in np.linspace(-90, 90, 180//rounding + 1):
            calc = (lati, longi)
            dicti[calc] = 0

    return dicti


def calc_loc(dicti, filename):
    """
    Calculates the latitude and longitude that the satellites are above, keeps a
    dictionary of the latitude and longitudes where the most satellites are near
    :param dicti: dictionary created with possible_coords
    :param filename: TLE data .txt filename
    :return: dictionary of the latitude and longitudes where the most satellites are near
    and the place at which the most satellites pass by
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
            print("First part: {}% done" .format(percent_done), end="\r")

    # Coordinates with most satellites
    place = max(dicti.items(), key=operator.itemgetter(1))[0]

    return dicti, place


def calc_angle(filename, place):
    """
    Calculates the angle that the laser should be able to reach
    :param filename: TLE data .txt filename
    :param place: the place of the laser in a (lat, long) tuple
    :return: highest_total - diameter of laser at highest point,
             angle_laser - the angle of the laser,
             minimum_distance - distance to closest satellite,
             maximum_distance - distance to furthest satellite
    """

    # initialize variables
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
            print("Second part: {}% done" .format(percent_done+1), end="\r")

    # Calculates the angle that the laser should be able to reach
    # takes the maximum distance between two satellites while they are both in
    # the range of the laser. Then calculates the height of the satellites minus
    # the radius of the earth, finally calculates the angle of the laser
    b = np.sqrt((best_i1[0])**2 + (best_i1[1])**2 + (best_i1[2])**2) - 6371
    c = np.sqrt((best_j1[0])**2 + (best_j1[1])**2 + (best_j1[2])**2) - 6371
    angle_laser = degrees(acos((b**2 + c**2 - highest_total**2)/(2.0 * b * c)))

    return highest_total, angle_laser, minimum_distance, maximum_distance

if __name__ == '__main__':
    """
    This main part combines all functions above and calculate the 
    best position to place the laser and the angle the laser should 
    be able to rotate to determine its range
    """

    # read file
    filename = open("data/cleaned_tle.txt", "r").read().splitlines()

    # start and finish time in year month day hour minute second
    start = datetime(2020, 1, 10, 14, 0, 0)
    finish = datetime(2020, 1, 10, 16, 0, 0)

    print("Starting calculation - Estimated time: 5 minutes")

    # calculate best place
    dicti, place = calc_loc(possible_coords(5), filename)

    print("Best place: {} - format: '(latitude, longitude)' \nWith {} satellites" .format(place, dicti[place]))

    # place = (80, -15)
    h, a, mini, maxi = calc_angle(filename, place)

    # print results
    print("\n\n- RESULTS -")
    print("Diameter of laser at highest point: {} km" .format(round(h, 1)))
    print("The angle of the laser: {} degrees" .format(round(a, 1)))
    print("Closest satellite: {} km" .format(round(mini, 1)))
    print("Furthest satellite: {} km" .format(round(maxi, 1)))
