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

def locate_sat(l1, l2, time1):
    satellite1 = twoline2rv(l1, l2, wgs72)
    time_list = (int(str(i)[0:4]), int(str(i)[5:7]), int(str(i)[8:10]),
        int(str(i)[11:13]), int(str(i)[14:16]), int(str(i)[17:19]))
    xyz, velocity = satellite1.propagate(time_list[0], time_list[1],
        time_list[2], time_list[3], time_list[4], time_list[5])
    return vector(xyz[1] * 1000, xyz[2] * 1000, xyz[0] * 1000)

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
satellite_prev = sphere(radius = 5e4, color = color.green)
satellite_new = sphere(radius = 5e4, color = color.red)
trail_prev = curve(color = color.yellow, radius = 5e3)
trail_new = curve(color = color.red, radius = 5e3)

start = datetime(2020, 1, 10, 14, 0, 0)
finish = datetime(2020, 1, 10, 15, 40, 0)
scene.autoscale = False

# Goes through all seconds of the given period and calculates the
# coordinates for those seconds
l1 = "1 40960U 15057C   20007.44139355 -.00000003  00000-0  71598-5 0  9999"
l2 = "2 40960  97.8791  76.7228 0017294 316.1151  43.8685 14.73392187228703"
hit = False
for j in range(5):
    rate(500)
    for i in hourly_it(start, finish):
        if j > 1 and hit == True:
            satellite_new.pos = locate_sat(l1_new, l2_new, i)
            trail_new.append(pos = satellite_new.pos)

        lati, longi = lati_longi(l1, l2, i, 5)

        # changes the color to red if it passes the laser
        if (lati, longi) == (80, -15):
            hit = True
            l1_new = "1 44096U 19018U   20007.41181402  .00001050  00000-0  48137-4 0  9995"
            l2_new = "2 44096  97.4334  70.4394 0012102  35.1376 325.0656 15.22615790 42756"

        # Location of satellite
        satellite_prev.pos = locate_sat(l1, l2, i)
        trail_prev.append(pos = satellite_prev.pos)
