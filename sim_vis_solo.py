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




# --- SIMULATION & VISUALIZATION FOR 1 SATELLITE ---

# --- LOAD SATELLITES ---

# load satellites from TLE data and pick first one
print("Loading satellites from .txt file...")
satellites = create_sat_list(2500, "data/output.txt")
SAT1 = satellites[2081]
print("Done!\n----------------")


# --- SETUP VISUALIZATION ---

scene.fullscreen = True
scene.title = "Satellite Motion"
scene.background = color.black
scene.width = 1200
scene.height = 700

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


# set start position-time and determine simulation time
SAT1.set_position(2020, 1, 10, 14, 0, 0)
simulation_time = int((datetime(2020, 1, 10, 17, 20, 0) - datetime(2020, 1, 10, 14, 0, 0)).total_seconds())

# setup laser
# laser power parameters
Cm  = 400*10**(-6) # 400 N/MW (optimum according to article https://www.psi.ch/sites/default/files/import/lmx-interfaces/BooksEN/Claude_JPP_2010-1.pdf)
Fluence = 1000000 #J/m2
spot = (80, -15)
laser = Laser(80, -15, spot=spot, Cm=Cm, fluence=Fluence)


for i in range(simulation_time):
    rate(500)

    if SAT1.already_crossed == False:
        lati, longi = SAT1.get_lat_long(rounding=5)
        SAT1.move_in_orbit(1)
        satellite_prev.pos = vector(SAT1.y * 1000, SAT1.z * 1000, SAT1.x * 1000)
        trail_prev.append(pos=satellite_prev.pos)

        # calculating hit duration
        SAT1.prev_duration = SAT1.hit_duration


        if (lati, longi) == laser.spot:
            SAT1.hit = True
            SAT1.hit_duration += 1



    # hit is done after hit_duration
    if SAT1.hit_duration == SAT1.prev_duration and SAT1.hit == True and SAT1.hit_done == False:
        SAT1.already_crossed = True
        # hit satellite with laser, let prev_sat carry on
        prev_SAT = laser.hit_satellite(SAT1, SAT1.hit_duration)

        SAT1.hit_done = True


    # when the hit actual hit is done
    if SAT1.hit_done == True:

        prev_SAT.move_in_orbit(1)
        satellite_prev.pos = vector(prev_SAT.y * 1000, prev_SAT.z * 1000, prev_SAT.x * 1000)
        trail_prev.append(pos=satellite_prev.pos)
        SAT1.move_in_orbit(1)
        satellite_new.pos = vector(SAT1.y * 1000, SAT1.z * 1000, SAT1.x * 1000)
        trail_new.append(pos=satellite_new.pos)
        height_from_earth = SAT1.calc_height()[1]
        if height_from_earth < 350:
            satellite_new.color = color.orange
            trail_new.color = color.orange



