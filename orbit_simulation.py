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

TEST = satellites[0]
TEST.set_position(2019, 12, 12, 12, 12, 12)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

col = 'blue'
simulation_time = 15000



# laser power parameters
Cm  = 400*10**(-6) # 400 N/MW (optimum according to article https://www.psi.ch/sites/default/files/import/lmx-interfaces/BooksEN/Claude_JPP_2010-1.pdf)
Fluence = 150000

laser = Laser(19.562170632009686, -130.47357933714184, 1, Cm, Fluence)

# simulation to configure laser
heights = []
for i in range(simulation_time):
    TEST.move_in_orbit(1)


    heights.append(TEST.calc_height()[1])

    ax.scatter(TEST.x, TEST.y, TEST.z, s=20, c=col, marker='.')

    if i == 7300:
        print("LASER HIT")

        print(TEST.calc_velocity())

        newV = laser.hit_satellite(TEST, 60)
        print("new velocity = ", newV)


        col = 'red'





print("\nCreating figure...")
plt.savefig('plots/sim.png')
print("Figure saved in plots/sim.png!")
