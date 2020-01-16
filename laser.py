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
import ephem

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
		"""
		This function uses ephem to calculate the distance between the laser
		and a satellite object
		:param satellite:
		:return: distance between laser and satellite object in kilometers
		"""

		# create laser as observer
		laser = ephem.Observer()
		laser.lon = str(self.long)
		laser.lat = str(self.lat)
		laser.elevation = -4338
		year, month, day, hour, minutes, sec = satellite.orbital_time
		laser.date = datetime(year, month, day, hour, minutes, sec)

		# calculate distance between observer and satellite
		tle_rec = ephem.readtle("SAT", satellite.l1, satellite.l2)
		tle_rec.compute(laser)
		d = tle_rec.range


		return d/1000


	def calc_velocity_change(self):
		return 0




	def hit_satellite(satellite: Satellite, duration, velocity_change):

		for i in range(duration):
			satellite.change_mean_motion(0.1)

			print(satellite.get_position_and_velocity[1])


		return satellite


		