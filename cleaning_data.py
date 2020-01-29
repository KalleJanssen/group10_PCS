from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

"""
------------------------------------------------------------------------------------
This file removes TLE data that returns errors and satellites not in low Earth orbit
and outputs a cleaned .txt file
------------------------------------------------------------------------------------
"""

def within_bounds(tuple_xyz):
    """
    This function determines whether the given coordinate
	is inside or outside the low Earth orbit (LEO).
	:param tuple_xyz: x, y, z coordinates of satellite
	:return: False if a coordinate is clearly outside of
	lower earth orbit, True otherwise
	"""

    for coord in tuple_xyz:
        if coord < -9000 or coord > 9000:
            return False
    return True


def clean_data(filename):
	"""
	This functions takes an TLE-formatted file as input and removes TLE data
	that provides errors or outliers
	:param filename: name of the TLE-formatted .txt file to be cleaned
	:return: nothing, but creates a cleaned version of the given
	.txt file in the data folder, named 'cleaned_tle.txt'
	"""

	# read data
	f = open(filename, "r").read().splitlines()
	open('data/cleaned_tle.txt', 'w').close()

	# goes through all data
	print("Cleaning data...", end="\r")
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
			with open("data/cleaned_tle.txt", "a") as text_file:
				text_file.write(l1)
				text_file.write("\n")
				text_file.write(l2)
				text_file.write("\n")

	print("Cleaned data written to 'cleaned_tle.txt'!")

# test
if __name__ == '__main__':
	clean_data("data/tle.txt")
