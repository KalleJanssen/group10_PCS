import matplotlib.pyplot as plt
import numpy
import time
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt



"""
This Class contains a Satellite object, with its positions and TLE data


To create the object, first use the get_satellite_from_TLE or 
get_list_of_sat_pos_objs function to get the sat_pos_obj


NOTE: The in the TLE-file stated orbital angles and other complex space numbers will be added

"""


class Satellite(object):
	def __init__(self, TLE_l1, TLE_l2, sat_pos_obj, height, width, length, mass, cross_section):
		self.sat_pos_obj = sat_pos_obj
		self.x = 0
		self.y = 0
		self.z = 0
		self.sat_number = sat_pos_obj.satnum
		self.l1 = TLE_l1
		self.l2 = TLE_l2
		self.orbital_time = (0, 0, 0, 0, 0, 0)


	def set_position(self, year, month, day, hour, minutes, sec):

		self.orbital_time = (year, month, day, hour, minutes, sec)


		position = self.sat_pos_obj.propagate(year, month, day, hour, minutes, sec)[0] 
		self.x = position[0]
		self.y = position[1]
		self.z = position[2]

		return position

	def get_position_and_velocity(self):

		# get position
		year, month, day, hour, minutes, sec = self.orbital_time
		position, velo = self.sat_pos_obj.propagate(year, month, day, hour, minutes, sec)

		# calculate velocity from vector components
		velocity = np.sqrt(velo[0]**2 + velo[1]**2 +velo[2]**2) * 3600

		return position, velocity

	def move_in_orbit(self, seconds):

		# change orbital time attribute
		year, month, day, hour, minutes, sec = self.orbital_time
		new_orbital_time = (year, month, day, hour, minutes, sec+seconds)
		self.orbital_time = new_orbital_time

		# calculate new position and set attributes
		new_position, velocity = self.sat_pos_obj.propagate(year, month, day, hour, minutes, self.orbital_time[5])
		self.x = new_position[0]
		self.y = new_position[1]
		self.z = new_position[2]

		# return new position

		return new_position


	def change_mean_motion(self, x):


		# add x change to mean motion in correct format
		mean_motion = float(self.l2[52:63])
		mean_motion = '{:.8f}'.format(mean_motion + x)
		mean_motion = list(mean_motion)



		# get it back in right TLE format
		l2_listed = list(self.l2)
		l2_listed[52:63] = mean_motion


		self.l2 = ''.join(map(str, l2_listed))

		prev_pos_obj = self.sat_pos_obj
		# object orbit has changed, create new sat_pos_obj

		self.sat_pos_obj = twoline2rv(self.l1, self.l2, wgs72)

		return self.sat_pos_obj




	def change_velocity(self, d_velocity, C_0m):
		# this function uses mathematical space model to change velocity and
		# other values in the TLE data to change the satellite's orbit/eject it
		# From this new TLE data, a new pos obj can be created
		new_pos_obj = 0

		return new_velo, old_velo



	def get_tle_lines(self):
		return self.l1, self.l2
















