import numpy as np
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

def tle_to_positions(filename):

	"""
	This functions takes an TLE-formatted file as input and returns the geological
	position and velocity of the object.
	"""
	f = open(filename, "r").read().splitlines()
	error1 = 0
	open('output.txt', 'w').close()
	for line in f:
		if line[0] == '1':
			l1 = line
			continue
		if line[0] == '2':
			l2 = line

		satellite = twoline2rv(l1, l2, wgs72)

		if satellite.error != 0:
			error1 += 1
		else:
			with open("output.txt", "a") as text_file:
				text_file.write(l1)
				text_file.write("\n")
				text_file.write(l2)
				text_file.write("\n")
	return 1


# test
if __name__ == '__main__':
	tle_to_positions("tle.txt")
