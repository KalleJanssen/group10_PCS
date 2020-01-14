from satellite import Satellite
from sat_simulation import get_list_of_sat_pos_objs
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
simulation_time = 14000


for i in range(simulation_time):

	print(" Progress: {0:.2f} of 100%".format(i / simulation_time * 100), end="\r")
	TEST.move_in_orbit(1)
	position, velocity = TEST.get_position_and_velocity()




	ax.scatter(TEST.x, TEST.y, TEST.z, s=20, c=col, marker='.')

	if i == 3600:
		TEST.change_mean_motion(-1.0)
		col = 'red'




plt.savefig('plots/sim.png')




