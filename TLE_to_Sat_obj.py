from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from satellite import Satellite

"""
------------------------------------------------------------------------------------
This file contains functions that read-in the TLE data and convert it into
Satellite objects from the Satellite class (satellite.py).
The final conversion to a list of Satellite objects is done with 'create_sat_list'.
------------------------------------------------------------------------------------
"""


def get_satellite_from_TLE(index, filename):
	"""
	This function takes an index and a filename and returns
	the satellite object of sgp4 (called satellite_pos_obj)
	at the given index in the TLE file.
	:param index: index of satellite in TLE file
	:param filename: name of TLE .txt file
	:return: satellite_pos_obj - position object for satellite,
								 created with sgp4 module
			 l1 - TLE line 1 of satellite
			 l2 - TLE line 2 of satellite
	"""

	# loop through file and find satellite at given index
	f = open(filename, "r").read().splitlines()

	count = 0
	for line in f:
		if count == index:
			l1 = line
			l2 = f[index+1]
			break

		count += 1

	# get sgp4 satelite position object
	satellite_pos_obj = twoline2rv(l1, l2, wgs72)

	return satellite_pos_obj, l1, l2




def get_list_of_sat_pos_objs(amount, filename):
	"""
	This function creates a list of satellite position objects
	(created with sgp4 module) from the given TLE file.
	:param amount: number of satellites to take from file
	:param filename: name of TLE .txt file
	:return: list of sgp4 satellite position objects
	"""

	# amount *2 because each satellite has two lines (TLE means: Two Line Element set)
	amount = amount * 2
	sat_pos_obj_list = []

	# for each index in the file, create a satellite position object
	# using the get_satellite_from_TLE and put it into the list
	for i in range(0, amount, 2):
		satellite_pos_obj, TLE_l1, TLE_l2 = get_satellite_from_TLE(i, filename)
		sat_pos_obj_list.append((satellite_pos_obj, TLE_l1, TLE_l2))

	return sat_pos_obj_list



def create_sat_list(amount, filename):
	"""
	This functions uses above functions to create a list
	of Satellite objects (satellite.py), that are being used
	in the simulation
	:param amount: number of satellites to take from file
	:param filename: name of TLE .txt file
	:return: list of Satellite objects
	"""

	# get list of sgp4 satellite position object
	sat_pos_objs = get_list_of_sat_pos_objs(amount, filename)

	# create list of satellite objects
	sat_list = []
	for obj in sat_pos_objs:
		pos_obj = obj[0]
		l1 = obj[1]
		l2 = obj[2]
		sat = Satellite(l1, l2, pos_obj)
		sat_list.append(sat)

	return sat_list

