from satellite import Satellite
from sat_simulation import get_list_of_sat_pos_objs
import time
import matplotlib.pyplot as plt

sat_pos_objs = get_list_of_sat_pos_objs(20, "data/output.txt")


def create_sat_list(sat_pos_objs):
	sat_list = []
	for obj in sat_pos_objs:
		# create satellite and set position
		sat = Satellite(obj, 1, 1, 1, 3000, 25)
		sat.set_position(2019, 12, 12, 12, 12, 12)
		sat_list.append(sat)

	return sat_list


# SIMULATION
satellites = create_sat_list(sat_pos_objs)

simulation_time = 140

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# start simulation
start = time.time()
for i in range(simulation_time):
	print("Seconds: {}".format(i), end="\r")
	for sat in satellites:
		sat.move_in_orbit(1)
		print(sat.x, sat.y, sat.x)
		ax.scatter(sat.x, sat.y, sat.z, c='black', marker='.', lw=0)


plt.savefig('plots/sim.png')
elapsed_time = (time.time() - start)

print("\n\n Elapsed time:", elapsed_time/60, "minutes6")
