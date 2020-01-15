import matplotlib.pyplot as plt
import numpy
import time
from satellite import Satellite
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import geopy.distance


"""
This class contains a Laser object

"""



class Laser(object):
	def __init__(self, latitude, longitude, max_power, beam_range, spot_size):
		self.long = longitude
		self.lat = latitude
		self.max_power = max_power
		self.range = beam_range
		self.spot_size = spot_size


	def sat_distance(self, satellite: Satellite):
		lat_sat, long_sat = satellite.get_lat_long()
		coords_sat = (lat_sat, long_sat)
		coords_laser = (self.lat, self.long)
		surface_d = geopy.distance.vincenty(coords_sat, coords_laser).km
		sat_height = satellite.calc_height()[1]

		d = np.sqrt(surface_d**2 + sat_height**2)

		return d


	def calc_velocity_change(self):
		return 0




	def hit_satellite(satellite: Satellite, duration, velocity_change):

		for i in range(duration):
			satellite.change_mean_motion(0.1)

			print(satellite.get_position_and_velocity[1])


		return satellite_object


		