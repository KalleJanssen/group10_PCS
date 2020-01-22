"""
Simulate the satellites around the globe, satellites turn red when they pass
the area that the laser can reach.
"""

from __future__ import division
from vpython import *
import datetime
from datetime import datetime, timedelta
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from best_position import *
from where_and_parameters import *

filename = open("data/output.txt", "r").read().splitlines()

scene.title = "Satellite Motion"

scene.background = color.black

# Calculate xyz coordinates from longitude and latitude
r = 6378137
x = r*cos(80)*cos(-15)
y = r*cos(80)*sin(-15)
z = -r*sin(80) * (1 - 1/298.257223563)

# place the cone
length = (mag(vector(y,z,x)) + 2000000) / mag(vector(y,z,x))
cone(pos=vector(-x-350000,z,y+200000) * length,
     axis=vector(x,-z,-y),
     size=vector(2200000,1000000,1000000),
     color=color.red, opacity=0.5)

# add the earth
earth = sphere(radius = 6.378e6, texture=textures.earth)
d = {}

# make satellites
for i in range(len(filename)//2):
    d["satellite{}" .format(i)] = sphere(radius = 5e4, color = color.green)

start = datetime(2020, 1, 10, 14, 0, 0)
finish = datetime(2020, 1, 10, 16, 0, 0)
scene.autoscale = False
total = 0
list_line = []

# Goes through all seconds of the given period and calculates the
# coordinates for those seconds
for i in hourly_it(start, finish):
    index = 0
    rate(len(filename))

    for line in filename:
        if line[0] == '1':
            l1 = line
            continue
        if line[0] == '2':
            index += 1
            l2 = line

        lati, longi = lati_longi(l1, l2, i, 5)

        # changes the color to red if it passes the laser
        if (lati, longi) == (80, -15):
            if line not in list_line:
                total += 1
                satellite = d["satellite{}" .format(index)]
                satellite.visible = False
                del satellite
                d["satellite{}" .format(index)] = sphere(radius = 5e4, color = color.red)
                list_line.append(line)

        # Location of satellite
        satellite1 = twoline2rv(l1, l2, wgs72)
        time_list = (int(str(i)[0:4]), int(str(i)[5:7]), int(str(i)[8:10]),
            int(str(i)[11:13]), int(str(i)[14:16]), int(str(i)[17:19]))
        xyz, velocity = satellite1.propagate(time_list[0], time_list[1],
            time_list[2], time_list[3], time_list[4], time_list[5])
        satellite = d["satellite{}" .format(index)]
        satellite.pos = vector(xyz[1] * 1000, xyz[2] * 1000, xyz[0] * 1000)

        if index == len(filename)//2 - 1:
            scene.caption = "\n {} out of {} satellites hit by the laser" .format(total, len(filename)//2)
            break
