# pip install sgp4
# https://pypi.org/project/sgp4/

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

def hourly_it(start, finish):
    """
    Returns a list of all timepoints between a start and end date
    """
    while finish > start:
        start = start + timedelta(seconds=1)
        yield start

def get_position(time_list, filename):
    """
    Calculates all positions of all satellites at a specific time
    """
    position_list = []
    for line in filename:
        if line[0] == '1':
            l1 = line
            continue
        if line[0] == '2':
            l2 = line

        # Calculates position of a single satellite
        satellite = twoline2rv(l1, l2, wgs72)
        position, velocity = satellite.propagate(time_list[0], time_list[1],
            time_list[2], time_list[3], time_list[4], time_list[5])
        position_list.append(position)
    return position_list

def cycle_through_time(start, finish, filename):
    """
    Adds the positions of all satellites to a dictionary with a specific time
    """
    position_dict = {}
    for hour in hourly_it(start, finish):

        # time_list is a tuple consisting of year month day hour minute second
        time_list = (int(str(hour)[0:4]), int(str(hour)[5:7]), int(str(hour)[8:10]),
        int(str(hour)[11:13]), int(str(hour)[14:16]), int(str(hour)[17:19]))
        position_dict[hour] = get_position(time_list, filename)
    return position_dict

def plot_satellites(coord_list):
    """
    Plots the positions of the satellites in a scatterplot
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = [i[0] for i in final_list]
    ys = [i[1] for i in final_list]
    zs = [i[2] for i in final_list]
    ax.scatter(xs, ys, zs)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.savefig('plots/foo.png')

filename = open("data/output.txt", "r").read().splitlines()
position_dict = {}
error1 = 0

# start and finish time in year month day hour minute second
start = datetime(2012, 10, 2, 12, 0, 0)
finish = datetime(2012, 10, 2, 12, 0, 1)

dicti = cycle_through_time(start, finish, filename)
final_list = list(dicti.values())[0]

plot_satellites(final_list)
