import numpy as np
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

def tle_to_positions(filename):
	f = open(filename, "r").read().splitlines()
	
	for line in f:
		if line[0] == '1':
			l1 = line
			continue
		if line[0] == '2':
			l2 = line





		satellite = twoline2rv(l1, l2, wgs72)
		position, velocity = satellite.propagate(2000, 6, 29, 12, 50, 19) # 12:50:19 on 29 June 2000n

		if satellite.error != 0:
			print("An error occurred: ", satellite.error_message)  
		

		print(position)
		print(velocity)		

		
		
	


if __name__ == '__main__':
	tle_to_positions("tle.txt")