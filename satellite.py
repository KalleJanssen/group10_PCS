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
This Class contains a satellite object, with its positions and spatial sctructure


To create the object, first use the get_satellite_from_TLE or 
get_list_of_sat_pos_objs function to get the sat_pos_obj


NOTE: The in the TLE-file stated orbital angles and other complex space numbers will be added

"""



class Satellite(object):
	def __init__(self, sat_pos_obj, height, width, length, mass, cross_section):
		self.sat_pos_obj = sat_pos_obj
		self.x = 0
		self.y = 0
		self.z = 0
		self.height = height
		self.width = width
		self.length = length
		self.mass = mass
		self.cross_section = cross_section
		self.sat_number = sat_pos_obj.satnum
		self.orbital_time = (0, 0, 0, 0, 0, 0)

	

	def set_position(self, year, month, day, hour, minutes, sec):

		self.orbital_time = (year, month, day, hour, minutes, sec)


		position = self.sat_pos_obj.propagate(year, month, day, hour, minutes, sec)[0] 
		self.x = position[0]
		self.y = position[1]
		self.z = position[2]

		return position

	def move_in_orbit(self, seconds):

		# change orbital time attribute
		year, month, day, hour, minutes, sec = self.orbital_time
		new_orbital_time = (year, month, day, hour, minutes, sec+seconds)
		self.orbital_time = new_orbital_time


		# calculate new position and set attributes
		new_position = self.sat_pos_obj.propagate(year, month, day, hour, minutes, self.orbital_time[5])[0]
		self.x = new_position[0]
		self.y = new_position[1]
		self.z = new_position[2]

		# return new position

		return new_position









