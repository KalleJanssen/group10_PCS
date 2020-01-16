from satellite import Satellite
from sat_simulation import get_list_of_sat_pos_objs
from laser import Laser
import time
import numpy as np
import numpy
import time
import difflib
from checksum import verify_checksum, fix_checksum
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

sat_pos_objs = get_list_of_sat_pos_objs(20, "data/output.txt")
print(sat_pos_objs)

def create_sat_list(sat_pos_objs):
    sat_list = []
    for obj in sat_pos_objs:
        # create satellite and set position

        pos_obj = obj[0]
        l1 = obj[1]
        l2 = obj[2]
        sat = Satellite(l1, l2, pos_obj, 1, 1, 1, 3000, 25)
        sat.set_position(2019, 12, 12, 12, 12, 12)
        sat_list.append(sat)

    return sat_list

# SIMULATION
satellites = create_sat_list(sat_pos_objs)

TEST = satellites[1]
TEST.set_position(2019, 12, 12, 12, 12, 12)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

col = 'blue'
simulation_time = 100


laser = Laser(19.562170632009686 , -130.47357933714184, 1, 1, 1, 100*10**(-6), 1)



for i in range(simulation_time):
    TEST.move_in_orbit(1)
    velocity = TEST.calc_velocity()
    height_surface = TEST.calc_height()

    lat, lon  = TEST.get_lat_long()

    #print(lat, lon)
    #print(laser.lat, laser.long)

    d = laser.sat_distance(TEST)

    #print("Distance from laser to satellite:", d, "\n Height:", TEST.calc_height()[1])

    ax.scatter(TEST.x, TEST.y, TEST.z, s=20, c=col, marker='.')

    if i == 60:
        print("LASER HIT")
        dV = laser.calc_velocity_change(TEST, 30)
        print(dV)
        TEST.change_mean_motion(1.0)
        col = 'red'



print("\nCreating figure...")
plt.savefig('plots/sim.png')
print("Figure saved in plots/sim.png!")
