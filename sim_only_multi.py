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

print("Loading satellites from .txt file...")
satellites = create_sat_list(3000, "data/output.txt")
print("Done!\n----------------")

print("Initializing satellites...")
# set start position-times and determine simulation time
for sat in satellites:
    sat.set_position(2020, 1, 10, 14, 0, 0)
print("Done!\n----------------")


simulation_time = int((datetime(2020, 1, 11, 14, 0, 0) - datetime(2020, 1, 10, 14, 0, 0)).total_seconds())


print("Setting up laser...")
# setup laser
# laser power parameters
Cm  = 400*10**(-6) # 400 N/MW (optimum according to article https://www.psi.ch/sites/default/files/import/lmx-interfaces/BooksEN/Claude_JPP_2010-1.pdf)
Fluence = 1000000 #J/m2
spot = (80, -15)
laser = Laser(80, -15, spot=spot, Cm=Cm, fluence=Fluence)
print("Done!\n----------------")


print("Simulation started! \n")

n_burned = 0
n_hits = 0
n_sats = len(satellites)
for i in range(simulation_time):

    print("Progress: {:.2f}% --- Hits: {} / {} --- Burned in atmosphere: {} of {} hit satellites".format(i/simulation_time * 100, n_hits, n_sats, n_burned, n_hits), end="\r")

    for sat in satellites:
        if sat.already_crossed == False:
            lati, longi = sat.get_lat_long(rounding=5)
            sat.move_in_orbit(1)

            # calculating hit duration
            sat.prev_duration = sat.hit_duration

            if (lati, longi) == laser.spot:
                sat.hit = True
                sat.hit_duration += 1


        # hit is done after hit_duration
        if sat.hit_duration == sat.prev_duration and sat.hit == True and sat.hit_done == False:
            sat.already_crossed = True
            # hit satellite with laser, let prev_sat carry on
            prev_SAT = laser.hit_satellite(sat, sat.hit_duration)

            n_hits += 1
            sat.hit_done = True


        # when the hit actual hit is done
        if sat.hit_done == True:

            sat.move_in_orbit(1)

            height_from_earth = sat.calc_height()[1]

            if height_from_earth < 350:
                if sat.burned == False:
                    n_burned += 1
                sat.burned = True



print("Result: {:.2f}% --- Hits: {} / {} --- Burned in atmosphere: {} of {} hit satellites".format(i/simulation_time * 100, n_hits, n_sats, n_burned, n_hits))
