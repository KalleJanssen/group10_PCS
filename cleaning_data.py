import numpy as np
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

def within_bounds(x):
	"""
	returns True if value is between -8000 and 8000
	"""
	if x > -8000 and x < 8000:
		return True
	else:
		return False

def cleaned_data(filename):
	"""
	This functions takes an TLE-formatted file as input and removes TLE data
	that provides errors or outliers
	"""
	f = open(filename, "r").read().splitlines()
	error1 = 0
	open('output.txt', 'w').close()

	# goes through all data
	for line in f:
		if line[0] == '1':
			l1 = line
			continue
		if line[0] == '2':
			l2 = line

		# calculates the data from a saellite
		satellite = twoline2rv(l1, l2, wgs72)
		position, velocity = satellite.propagate(2010, 6, 29, 12, 50, 19)

		# writes to file if no error and satellite has expected xyz-coordinates
		if satellite.error != 0:
			error1 += 1
		elif within_bounds(position[0]) and within_bounds(position[1]) and within_bounds(position[2]):
			with open("output.txt", "a") as text_file:
				text_file.write(l1)
				text_file.write("\n")
				text_file.write(l2)
				text_file.write("\n")
		else:
			error1 += 1
	return 1


# test
if __name__ == '__main__':
	cleaned_data("tle.txt")
