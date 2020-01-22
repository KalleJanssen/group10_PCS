from __future__ import division
from vpython import *
import datetime
from datetime import datetime, timedelta
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from best_position import *
from where_and_parameters import *

def hourly_it(start, finish):
    """
    Returns a list of all timepoints between a start and end date
    """
    while finish > start:
        start = start + timedelta(seconds=1)
        yield start
filename = open("data/output.txt", "r").read().splitlines()

### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

# Set window title
scene.title = "Satellite Motion"

# Make scene background black
scene.background = color.black

# Define scene objects (units are in meters)
earth = sphere(radius = 6.378e6, texture=textures.earth)
d = {}
e = {}
for i in range(len(filename)//2):
    e["trial{}" .format(i)] = curve(color = color.yellow, radius = 5e3)
    d["satellite{}" .format(i)] = sphere(radius = 5e4, color = color.green)


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------
start = datetime(2020, 1, 10, 14, 0, 0)
finish = datetime(2020, 1, 17, 14, 0, 0)
scene.autoscale = False
plot1 = 0
total = 0
list_line = []
for i in hourly_it(start, finish):
    #scene.waitfor('click')
    index = 0
    plot1 += 1
    rate(3005)

    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    for line in filename:
        if line[0] == '1':
            l1 = line
            continue
        if line[0] == '2':
            index += 1
            l2 = line

        lati, longi = lati_longi(l1, l2, i, 5)

        if (lati, longi) == (80, -15):
            if line not in list_line:
                total += 1
                satellite = d["satellite{}" .format(index)]
                satellite.visible = False
                e["trial{}" .format(index)] = curve(color = color.red, radius = 5e3)
                d["satellite{}" .format(index)] = sphere(radius = 5e4, color = color.red)
                list_line.append(line)

        satellite1 = twoline2rv(l1, l2, wgs72)
        time_list = (int(str(i)[0:4]), int(str(i)[5:7]), int(str(i)[8:10]),
            int(str(i)[11:13]), int(str(i)[14:16]), int(str(i)[17:19]))
        xyz, velocity = satellite1.propagate(time_list[0], time_list[1],
            time_list[2], time_list[3], time_list[4], time_list[5])

        satellite = d["satellite{}" .format(index)]
        satellite.pos = vector(xyz[1] * 1000, xyz[2] * 1000, xyz[0] * 1000)
        trial = e["trial{}" .format(index)]
        trial.append(pos = satellite.pos)

        if index == 1:
            scene.caption = "\n {} out of {} satellites hit by the laser" .format(total, len(filename)//2)
            break
