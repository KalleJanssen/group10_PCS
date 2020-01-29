from vpython import *
from TLE_to_Sat_obj import *
from datetime import datetime
from laser import Laser

"""
------------------------------------------------------------------------------------
SIMULATION AND VISUALIZATION FOR ONE SATELLITE

In this file the simulation and visualization for 1 satellite is being done. 
The visualization is visible in a local web page, which opens automatically.
You can rotate the earth and zoom in with your mouse and the red cone represents the 
laser.
The orbit and the new orbit of the satellite are dynamically shown.
------------------------------------------------------------------------------------
"""

# --- LOAD SATELLITES ---

# load satellites from TLE data and pick one that goes through the laser
print("Loading satellites from .txt file...")
satellites = create_sat_list(3002, "data/cleaned_tle.txt")
SAT1 = satellites[2081]
print("Done!\n----------------")


# --- SETUP VISUALIZATION ---

print("Started simulation and visualization!")
print("Press CTRL+C to stop simulation and visualization.")

# setup scene
scene.fullscreen = True
scene.title = "Satellite orbiting the Earth and being hit by laser"
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

# make satellites (initialize orbit and orbit after hit)
satellite_prev = sphere(radius = 5e4, color = color.green)
satellite_new = sphere(radius = 5e4, color = color.red)
trail_prev = curve(color = color.yellow, radius = 50e3)
trail_new = curve(color = color.red, radius = 50e3)
scene.autoscale = False


# --- SETUP SATELLITES ---

# set start position-time and determine simulation time
SAT1.set_position(2020, 1, 10, 14, 0, 0)

# more than 2 hours in order to make the new orbit 100% visible
simulation_time = int((datetime(2020, 1, 10, 18, 0, 0) - datetime(2020, 1, 10, 14, 0, 0)).total_seconds())


# --- SETUP LASER ---

# set laser power parameters
Cm  = 400*10**(-6) #N/MW
Fluence = 1000000 #J/cm2

# calculated with calc_laser_pos, in the code below we
# used rounding to determine whether a satellite is within
# the lasers range (and is being hit)
laser_range = (80, -15)

# create Laser object
laser = Laser(80, -15, range=laser_range, Cm=Cm, fluence=Fluence)


# --- SIMULATE AND VISUALIZE ---

for i in range(simulation_time):
    rate(500)

    if SAT1.already_crossed == False:
        lati, longi = SAT1.get_lat_long(rounding=5)

        # move 1 second in orbit
        SAT1.move_in_orbit(1)

        # update position of visual trail and dot
        satellite_prev.pos = vector(SAT1.y * 1000, SAT1.z * 1000, SAT1.x * 1000)
        trail_prev.append(pos=satellite_prev.pos)

        # calculating hit duration
        SAT1.prev_duration = SAT1.hit_duration

        # when the satellite is in the range of the laser
        if (lati, longi) == laser.range:
            SAT1.hit = True
            SAT1.hit_duration += 1


    # when the satellite is in the laser, hit it!
    if SAT1.hit_duration == SAT1.prev_duration and SAT1.hit == True and SAT1.hit_done == False:
        SAT1.already_crossed = True

        # hit satellite with laser, let prev_sat carry on
        prev_SAT = laser.hit_satellite(SAT1, SAT1.hit_duration)

        # hit is done after hit_duration
        SAT1.hit_done = True


    # when the actual hit is done
    if SAT1.hit_done == True:

        # draw new orbit and finish old orbit
        prev_SAT.move_in_orbit(1)
        satellite_prev.pos = vector(prev_SAT.y * 1000, prev_SAT.z * 1000, prev_SAT.x * 1000)
        trail_prev.append(pos=satellite_prev.pos)
        SAT1.move_in_orbit(1)
        satellite_new.pos = vector(SAT1.y * 1000, SAT1.z * 1000, SAT1.x * 1000)
        trail_new.append(pos=satellite_new.pos)

        # change to orange when at unstable height (atmospheric drag)
        # and eventually burned in atmosphere
        height_from_earth = SAT1.calc_height()[1]
        if height_from_earth < 350:
            satellite_new.color = color.orange
            trail_new.color = color.orange



