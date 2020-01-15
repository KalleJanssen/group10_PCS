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



"""
This class contains a Laser object

"""



class Laser(object):
	def __init__(self, longitude, latitude, power, beam_range, spot_size):
		self.longitude = longitude
		self.latitude = latitude
		self.power = power
		self.range = beam_range
		self.spot_size = spot_size


	def sat_distance(self, satellite: Satellite):


	def calc_velocity_change(self):




	def hit_satellite(satellite_object, duration, calc_velocity_change):

		for i in range(duration):
			satellite_object.change_mean_motion(0.1)

			print(satellite_object.get_position_and_velocity[1])


		return satellite_object


		