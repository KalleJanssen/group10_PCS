import matplotlib.pyplot as plt
import numpy
import time
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from satellite import Satellite




def get_satellite_from_TLE(index, filename):
	"""
	This function takes an index and a filename and returns
	the satellite object of sgp4 (called satellite_pos_obj)
	at the given index in the TLE file.
	"""

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

	return satellite_pos_obj, l1, l2




def get_list_of_sat_pos_objs(amount, filename):
	"""
	This function returns a list of sgp4 satellite object from
	the given TLE file, where the argument 'amount' determines
	the number of satellites in the list
	"""

	amount = amount * 2
	sat_pos_obj_list = []

	for i in range(0, amount, 2):
		satellite_pos_obj = get_satellite_from_TLE(i, filename)[0]
		TLE_l1 = get_satellite_from_TLE(i, filename)[1]
		TLE_l2 = get_satellite_from_TLE(i, filename)[2]

		sat_pos_obj_list.append((satellite_pos_obj, TLE_l1, TLE_l2))

	return sat_pos_obj_list



def create_sat_list(amount, filename):


	sat_pos_objs = get_list_of_sat_pos_objs(amount, filename)

	sat_list = []

	for obj in sat_pos_objs:
		pos_obj = obj[0]
		l1 = obj[1]

		l2 = obj[2]
		sat = Satellite(l1, l2, pos_obj)
		sat_list.append(sat)

	return sat_list

