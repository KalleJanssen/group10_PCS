import ephem
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import numpy as np
from ephem import degree
from datetime import datetime, timedelta
from checksum import fix_checksum

"""
------------------------------------------------------------------------------------
This Class contains a Satellite object, with its position, TLE data and other 
attributes needed for simulation
------------------------------------------------------------------------------------
"""

class Satellite(object):
	def __init__(self, TLE_l1, TLE_l2, sat_pos_obj):
		"""
		This function initalizes a satellite object for the simulation
		:param TLE_l1: line 1 of satellite data from TLE .txt file
		:param TLE_l2: line 2 of satellite data from TLE .txt file
		:param sat_pos_obj: satellite position object created with sgp4
		for orbit position calculation
		"""
		self.sat_pos_obj = sat_pos_obj
		self.x = 0
		self.y = 0
		self.z = 0
		self.sat_number = sat_pos_obj.satnum
		self.l1 = TLE_l1
		self.l2 = TLE_l2
		self.orbital_time = (0, 0, 0, 0, 0, 0)
		self.hit = False
		self.hit_done = False
		self.already_crossed = False
		self.burned = False
		self.prev_duration = 0
		self.hit_duration = 0



	def set_position(self, year, month, day, hour, minutes, sec):
		"""
		This function initializes a position at the given time using
		the sgp4 propagate function.
		The parameters below determine the time
		:param year:
		:param month:
		:param day:
		:param hour:
		:param minutes:
		:param sec:
		:return: x, y, z position of the satellite in space
		"""

		# calculates x, y, z position vector in space
		self.orbital_time = (year, month, day, hour, minutes, sec)
		position = self.sat_pos_obj.propagate(year, month, day, hour, minutes, sec)[0]

		# sets x, y, z positions
		self.x = position[0]
		self.y = position[1]
		self.z = position[2]

		return position

	def calc_height(self):
		"""
		This function calculates the height of a satellite above sea level
		using its x, y, z coordinates.
		:return: height from center to earth, height from surface of the earth
		"""

		# calculate height by taking vector length
		height_from_center = np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
		height_from_surface = height_from_center-6371

		return height_from_center, height_from_surface

	def calc_velocity(self):
		"""
		This function calculates the orbital velocity of a satellite
		using its x, y, z velocities.
		:return: the satellites orbital velocity
		"""

		# get position
		year, month, day, hour, minutes, sec = self.orbital_time
		velo = self.sat_pos_obj.propagate(year, month, day, hour, minutes, sec)[1]

		# calculate velocity from vector components
		velocity = np.sqrt(velo[0]**2 + velo[1]**2 +velo[2]**2) * 3600

		return velocity

	def get_lat_long(self, rounding=0, name="SAT"):
		"""
		This function returns the perpendicular point of satellite
		projected on earth's surface.
		:param name: can be ignored, not needed
		:return: projected longitude and latitude on Earth's surface
		"""

		# get latitude and longitude of satellite using its TLE
		# data and the Python Ephem module
		tle_rec = ephem.readtle(name, self.l1, self.l2)
		year, month, day, hour, minutes, sec = self.orbital_time
		time = datetime(year, month, day, hour, minutes, sec)
		tle_rec.compute(time)
		lati = (tle_rec.sublat / degree)
		longi = (tle_rec.sublong / degree)
		if rounding != 0:
			lati = rounding * round(lati / rounding)
			longi = rounding * round(longi / rounding)


		return lati, longi

	def move_in_orbit(self, seconds):
		"""
		This function move the satellite in its orbit
		:param seconds: how many second the satellite should move
		:return: the satellite's new space/orbit position
		"""

		# change orbital time attribute with timedelta
		year, month, day, hour, minutes, sec = self.orbital_time
		dt1 = datetime(year, month, day, hour, minutes, sec)
		dt2 = dt1 + timedelta(seconds=seconds)
		new_orbital_time = (dt2.year, dt2.month, dt2.day, dt2.hour, dt2.minute, dt2.second)
		self.orbital_time = new_orbital_time

		# calculate new position and set attributes
		new_position, velocity = self.sat_pos_obj.propagate(year, month, day, hour, minutes, self.orbital_time[5])
		self.x = new_position[0]
		self.y = new_position[1]
		self.z = new_position[2]

		return new_position


	def change_mean_motion(self, dV):
		"""
		This function changes the satellites mean motion, which
		influences it's orbital velocity. The velocity change
		results in a new orbit for the satellite
		:param dV: change of mean motion
		:return: new satellite-position object of the satellite
		"""

		# add x change to mean motion in correct format
		mean_motion = float(self.l2[52:63])
		mean_motion = '{:.8f}'.format(mean_motion + dV)
		mean_motion = list(mean_motion)

		# get it back in right TLE format
		l2_listed = list(self.l2)
		l2_listed[52:63] = mean_motion

		# fix TLE line 2 checksum
		self.l2 = fix_checksum(''.join(map(str, l2_listed)))

		# object orbit has changed, create new sat_pos_obj
		self.sat_pos_obj = twoline2rv(self.l1, self.l2, wgs72)

		return self.sat_pos_obj

	def height_sat(self, lati, longi):
		"""
		Returns distance from satellite object to a specific coordinate on earth (observer)
		:param lati: latitude of observer on earth
		:param longi: longitude of observer on earth
		:return: distance from observer to satellite
		"""

		# get orbital time of satellite in datetime-format
		year, month, day, hour, minutes, sec = self.orbital_time
		time = datetime(year, month, day, hour, minutes, sec)

		# calculate distance from satellite to observer in meters
		laser = ephem.Observer()
		tle_rec = ephem.readtle("name", self.l1, self.l2)
		tle_rec.compute(time)
		laser.lon = decdeg2dms(longi)
		laser.lat = decdeg2dms(lati)
		laser.elevation = 0
		laser.date = time
		tle_rec = ephem.readtle("SAT", self.l1, self.l2)
		tle_rec.compute(laser)

		# convert to kilometers
		d = tle_rec.range / 1000

		return d
