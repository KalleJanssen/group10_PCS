from TLE_to_Sat_obj import *
from laser import Laser
from datetime import datetime

"""
------------------------------------------------------------------------------------
SIMULATION ONLY FOR MULTIPLE SATELLITES

In this file the simulation for multiple satellite is being done. 
After running the final results are shown.
------------------------------------------------------------------------------------
"""

# --- SIMULATION ---

# --- LOAD SATELLITES ---

# load satellites from TLE data and pick first one
print("Loading satellites from .txt file...")
satellites = create_sat_list(3002, "data/cleaned_tle.txt")
print("Done!\n----------------")


# --- SETUP SATELLITES ---
print("Initializing satellites...")
# set start position-times and determine simulation time
for sat in satellites:
    sat.set_position(2020, 1, 10, 14, 0, 0)
print("Done!\n----------------")

# 2 hours
simulation_time = int((datetime(2020, 1, 10, 16, 0, 0) - datetime(2020, 1, 10, 14, 0, 0)).total_seconds())


# --- SETUP LASER ---

print("Setting up laser...")
# set laser power parameters
Cm  = 400*10**(-6) # N/MW
Fluence = 1000000 #J/cm2

# calculated with calc_laser_pos, in the code below we
# used rounding to determine whether a satellite is within
# the lasers range (and is being hit)
laser_range = (80, -15)

# create Laser object
laser = Laser(80, -15, range=laser_range, Cm=Cm, fluence=Fluence)

print("Done!\n----------------")


# --- SIMULATION ---

print("Simulation started! \n")

# intialize counts
n_burned = 0
n_hits = 0
n_sats = len(satellites)

for i in range(simulation_time):

    print("Progress: {:.2f}% --- Hits: {} / {} --- Burned in atmosphere: {} of {} hit satellites".format(i/simulation_time * 100, n_hits, n_sats, n_burned, n_hits), end="\r")

    for sat in satellites:
        if sat.already_crossed == False:
            lati, longi = sat.get_lat_long(rounding=5)

            # move 1 second in orbit
            sat.move_in_orbit(1)

            # calculating hit duration
            sat.prev_duration = sat.hit_duration

            # when the satellite is in the range of the laser
            if (lati, longi) == laser.range:
                sat.hit = True
                sat.hit_duration += 1


        # when the satellite is in the laser, hit it!
        if sat.hit_duration == sat.prev_duration and sat.hit == True and sat.hit_done == False:
            sat.already_crossed = True
            # hit satellite with laser, let prev_sat carry on
            prev_SAT = laser.hit_satellite(sat, sat.hit_duration)

            n_hits += 1

            # hit is done after hit_duration
            sat.hit_done = True

        # when the hit actual hit is done
        if sat.hit_done == True:

            sat.move_in_orbit(1)
            height_from_earth = sat.calc_height()[1]

            if height_from_earth < 350:
                if sat.burned == False:
                    n_burned += 1
                sat.burned = True



print("\n-Result-\nHits: {} / {}\nBurned in atmosphere: {} of {} hit satellites".format(i/simulation_time * 100, n_hits, n_sats, n_burned, n_hits))
