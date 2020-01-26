# Combine laser.py, satellite.py, where_and_parameters.py, earth_sim.py and best_position.py

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from vpython import *
from TLE_to_Sat_obj import *
from satellite import Satellite
from laser import Laser


# --- LOAD SATELLITES ---

# load satellites from TLE data and pick first one
satellites = create_sat_list(2500, "data/output.txt")
SAT1 = satellites[2081]
print(SAT1.sat_number)

# --- SETUP VISUALIZATION ---

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
scene.autoscale = False

# --- SIMULATION ---

# set start position-time and determine simulation time
SAT1.set_position(2020, 1, 10, 14, 0, 0)
simulation_time = int((datetime(2020, 1, 10, 17, 20, 0) - datetime(2020, 1, 10, 14, 0, 0)).total_seconds())

# setup laser
# laser power parameters
Cm  = 400*10**(-6) # 400 N/MW (optimum according to article https://www.psi.ch/sites/default/files/import/lmx-interfaces/BooksEN/Claude_JPP_2010-1.pdf)
Fluence = 1500000 #J/m2
spot = (80, -15)
laser = Laser(80, -15, spot=spot, Cm=Cm, fluence=Fluence)

hit = False
already_crossed = False
hit_done = False
prev_duration = 0
hit_duration = 0
for i in range(simulation_time):
    rate(1000)

    if already_crossed == False:
        lati, longi = SAT1.get_lat_long(rounding=5)
        SAT1.move_in_orbit(1)
        satellite_prev.pos = vector(SAT1.y * 1000, SAT1.z * 1000, SAT1.x * 1000)
        trail_prev.append(pos=satellite_prev.pos)

        # calculating hit duration
        prev_duration = hit_duration


        if (lati, longi) == laser.spot:
            hit = True
            hit_duration += 1



    # hit is done after hit_duration
    if hit_duration == prev_duration and hit == True and hit_done == False:
        already_crossed = True
        # hit satellite with laser, let prev_sat carry on
        prev_SAT = laser.hit_satellite(SAT1, hit_duration)

        hit_done = True


    # when the hit actual hit is done
    if hit_done == True:

        prev_SAT.move_in_orbit(1)
        satellite_prev.pos = vector(prev_SAT.y * 1000, prev_SAT.z * 1000, prev_SAT.x * 1000)
        trail_prev.append(pos=satellite_prev.pos)


        SAT1.move_in_orbit(1)
        satellite_new.pos = vector(SAT1.y * 1000, SAT1.z * 1000, SAT1.x * 1000)
        trail_new.append(pos=satellite_new.pos)






















    # # changes the color to red if it passes the laser
    # if count >= 1:
    #     hit = True
    #     laser.spot = (1000, 1000)
    #     laser.hit_satellite(SAT1, 10)
    #
    # # first make full orbit
    # if (lati, longi) == laser.spot:
    #     count += 1
    #
    # if hit == False:
    #     # Location of satellite
    #     satellite_prev.pos = vector(SAT1.y * 1000, SAT1.z * 1000, SAT1.x * 1000)
    #     trail_prev.append(pos=satellite_prev.pos)
    #
    #
    # if hit == True:
    #     satellite_new.pos = vector(SAT1.y * 1000, SAT1.z * 1000, SAT1.x * 1000)
    #     trail_new.append(pos=satellite_new.pos)
    #     sat_height = SAT1.calc_height()
    #     if sat_height[1] < 350:
    #         print("In atmosphere")

















