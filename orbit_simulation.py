from satellite import Satellite
from sat_simulation import get_list_of_sat_pos_objs
from laser import Laser
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy
import time
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt



sat_pos_objs = get_list_of_sat_pos_objs(2000, "data/output.txt")


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
simulation_time = 1400


for i in range(simulation_time):


    TEST.move_in_orbit(1)
    velocity = TEST.calc_velocity()
    height_center, height_surface = TEST.calc_height()

    print("Height from Earth's center:", height_center)
    print("Height from Earth's surface:", height_surface)

    ax.scatter(TEST.x, TEST.y, TEST.z, s=20, c=col, marker='.')

    if i == 700:
        print("LASER HIT")
        TEST.change_mean_motion(5.0)
        col = 'red'




plt.savefig('plots/sim.png')




