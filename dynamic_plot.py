import matplotlib.pyplot as plt
import numpy
import time
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


def get_satellite(index, filename):



	# loop through file and find satellite at given index
	positions = []
	f = open(filename, "r").read().splitlines()

	count = 0 
	for line in f:
		if count == index:

			l1 = line
			l2 = f[index+1]

			
			break
					
		count += 1


	# get sgp4 sattelite oobject
	satellite_pos_obj = twoline2rv(l1, l2, wgs72)
		

	return satellite_pos_obj




def get_position(satellite_pos_obj, time_sec):

		pos_obj = satellite_pos_obj.propagate(2019, 6, 29, 12, 50, time_sec)[0] # 12:50:19 on 29 June 2000n
		
		return pos_obj


def get_list_of_sat_pos_objs(amount, filename):

	amount = amount * 2
	sat_pos_obj_list = []

	for i in range(0, amount, 2):
		satellite_pos_obj = get_satellite(i, filename)
		sat_pos_obj_list.append(satellite_pos_obj)

	return sat_pos_obj_list





def simulate(filename, amount_of_satellites, simulation_time):
	sat_pos_obj_list  = get_list_of_sat_pos_objs(3000, "tle.txt")


	start = time.time()
	for i in range(simulation_time):
		print(i)
		for obj in sat_pos_obj_list:
			pos = get_position(obj, i)

			

	elapsed_time_fl = (time.time() - start) 
		
			
	return elapsed_time_fl


	
# test
if __name__ == '__main__':
	
	simulate("tle.txt", 3000, 120)
	

	




