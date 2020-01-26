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







# --- SIMULATION ---

# --- LOAD SATELLITES ---

# load satellites from TLE data and pick first one
satellites = create_sat_list(2500, "data/output.txt")



sats = []
for sat in satellites:
    sats.append((sat, sphere(radius = 5e4, color = color.green)))



# --- SETUP EARTH WITH LASER ---

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
scene.autoscale = False



# set start position-times and determine simulation time
for sat in sats:
    sat[0].set_position(2020, 1, 10, 14, 0, 0)

simulation_time = int((datetime(2020, 1, 10, 17, 20, 0) - datetime(2020, 1, 10, 14, 0, 0)).total_seconds())

# setup laser
# laser power parameters
Cm  = 400*10**(-6) # 400 N/MW (optimum according to article https://www.psi.ch/sites/default/files/import/lmx-interfaces/BooksEN/Claude_JPP_2010-1.pdf)
Fluence = 1000000 #J/m2
spot = (80, -15)
laser = Laser(80, -15, spot=spot, Cm=Cm, fluence=Fluence)


for i in range(simulation_time):
    rate(5000)

    for sat, visual in sats:

        if sat.already_crossed == False:
            lati, longi = sat.get_lat_long(rounding=5)
            sat.move_in_orbit(1)
            visual.pos = vector(sat.y * 1000, sat.z * 1000, sat.x * 1000)


            # calculating hit duration
            sat.prev_duration = sat.hit_duration


            if (lati, longi) == laser.spot:
                sat.hit = True
                visual.color = color.red
                sat.hit_duration += 1


        # hit is done after hit_duration
        if sat.hit_duration == sat.prev_duration and sat.hit == True and sat.hit_done == False:
            sat.already_crossed = True
            # hit satellite with laser, let prev_sat carry on
            prev_SAT = laser.hit_satellite(sat, sat.hit_duration)

            sat.hit_done = True


        # when the hit actual hit is done
        if sat.hit_done == True:


            sat.move_in_orbit(1)
            visual.pos = vector(sat.y * 1000, sat.z * 1000, sat.x * 1000)

            height_from_earth = sat.calc_height()[1]
            if height_from_earth < 350:
                visual.color = color.orange



