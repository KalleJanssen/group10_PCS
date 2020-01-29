from vpython import *
from TLE_to_Sat_obj import *
from datetime import datetime
from laser import Laser

"""
------------------------------------------------------------------------------------
SIMULATION AND VISUALIZATION FOR MULTIPLE SATELLITES

In this file the simulation and visualization for multiple satellite is being done. 
The visualization is visible in a local web page, which opens automatically.
You can rotate the earth and zoom in with your mouse and the red cone represents the 
laser.
The dynamically moving satellites and their state (hit, burned, not hit) are being 
showed around the earth. 

Green dot: not hit
Red dot: hit
Orange dot: hit and eventually burned in atmosphere
------------------------------------------------------------------------------------
"""

# --- SIMULATION ---

# --- LOAD SATELLITES ---
print("Loading satellites from .txt file...")
# load satellites from TLE data
satellites = create_sat_list(3002, "data/cleaned_tle.txt")
print("Done!\n----------------")

# --- SETUP EARTH VISUALIZATION WITH LASER AND SATELLITES ---

print("Started simulation and visualization!")
print("Press CTRL+C to stop simulation and visualization.")

# create satellite visualizations
sats = []
for sat in satellites:
    sats.append((sat, sphere(radius = 5e4, color = color.green)))

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
scene.autoscale = False

# --- SETUP SATELLITES ---

# set start position-times and determine simulation time
for sat in sats:
    sat[0].set_position(2020, 1, 10, 14, 0, 0)

# 2 hours
simulation_time = int((datetime(2020, 1, 10, 16, 0, 0) - datetime(2020, 1, 10, 14, 0, 0)).total_seconds())


# --- SETUP LASER ---

# set laser power parameters
Cm  = 400*10**(-6) # N/MW
Fluence = 1000000 #J/cm2

# calculated with calc_laser_pos, in the code below we
# used rounding to determine whether a satellite is within
# the lasers range (and is being hit)
laser_range = (80, -15)

# create Laser object
laser = Laser(80, -15, range=laser_range, Cm=Cm, fluence=Fluence)

# --- SIMULATE AND VISUALIZE ---

# initialize counts
n_burned = 0
n_hits = 0
n_sats = len(satellites)

for i in range(simulation_time):
    rate(1000)

    # update every satellite's position, every second
    for sat, visual in sats:
        scene.title = "Hits: {} / {} satellites\nBurned in atmosphere: {} of {} hit satellites".format(n_hits, n_sats, n_burned, n_hits)

        if sat.already_crossed == False:
            lati, longi = sat.get_lat_long(rounding=5)

            # move 1 second in orbit
            sat.move_in_orbit(1)

            # update position of visual object dot
            visual.pos = vector(sat.y * 1000, sat.z * 1000, sat.x * 1000)

            # calculating hit duration
            sat.prev_duration = sat.hit_duration

            # when the satellite is in the range of the laser
            if (lati, longi) == laser.range:
                sat.hit = True
                visual.color = color.red
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
            visual.pos = vector(sat.y * 1000, sat.z * 1000, sat.x * 1000)

            # change to orange when at unstable height (atmospheric drag)
            # and eventually burned in atmosphere
            height_from_earth = sat.calc_height()[1]
            if height_from_earth < 350:
                if sat.burned == False:
                    n_burned += 1
                sat.burned = True
                visual.color = color.orange



