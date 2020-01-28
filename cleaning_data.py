"""
Removes TLE data that returns errors and satellites not in low Earth orbit
"""

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

def within_bounds(tuple_xyz):
	"""
	returns False if a coordinate is clearly outside of lower earth orbit
	"""
	for coord in tuple_xyz:
		if coord < -9000 or coord > 9000:
			return False
	return True

def cleaned_data(filename):
	"""
	This functions takes an TLE-formatted file as input and removes TLE data
	that provides errors or outliers
	"""
	f = open(filename, "r").read().splitlines()
	open('data/output.txt', 'w').close()

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
		if satellite.error == 0 and within_bounds(position):
			with open("data/output.txt", "a") as text_file:
				text_file.write(l1)
				text_file.write("\n")
				text_file.write(l2)
				text_file.write("\n")


# test
if __name__ == '__main__':
	cleaned_data("data/tle.txt")
