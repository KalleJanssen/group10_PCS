# pip install sgp4
# https://pypi.org/project/sgp4/

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

def hourly_it(start, finish):
    while finish > start:
        start = start + timedelta(minutes=2)
        yield start

def plotting(l1, l2):
    start = datetime(2010, 10, 2, 12)
    finish = datetime(2010, 10, 2, 14)
    for hour in hourly_it(start, finish): # year month day hour minute second
        satellite = twoline2rv(l1, l2, wgs72)
        year = int(str(hour)[0:4])
        month = int(str(hour)[5:7])
        day = int(str(hour)[8:10])
        hour1 = int(str(hour)[11:13])
        minute = int(str(hour)[14:16])
        second = int(str(hour)[17:19])
        position, velocity = satellite.propagate(year, month, day, hour1, minute, second) # 12:50:19 on 29 June 2000n
        position_list.append(position)

        ax = plt.axes(projection='3d')

        # Data for a three-dimensional line
        xline = [i[0] for i in position_list]
        yline = [i[1] for i in position_list]
        zline = [i[2] for i in position_list]
        ax.plot3D(xline, yline, zline, 'gray')

f = open("tle.txt", "r").read().splitlines()
position_list = []
error1 = 0
for line in f:
    error1 += 1
    if line[0] == '1':
        l1 = line
        continue
    if line[0] == '2':
        l2 = line
    plotting(l1, l2)
    if error1 == 20:
        break
plt.savefig('foo.png')

