import ephem
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import numpy as np
from ephem import degree
from datetime import datetime, timedelta
from checksum import fix_checksum


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
		:return: sgp4 position-objectof satellite
		"""

		self.orbital_time = (year, month, day, hour, minutes, sec)

		position = self.sat_pos_obj.propagate(year, month, day, hour, minutes, sec)[0]
		self.x = position[0]
		self.y = position[1]
		self.z = position[2]

		return position

	def calc_height(self):
		"""
		This function calculates the height of a satellite above sea level
		using its x, y, z coordinates.
		:return: height from center to earth, heaft from surface of the earth
		"""

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

	def get_lat_long(self, name="SAT"):
		"""
		This function returns the perpendicular point of satellite
		projected on earth's surface.
		:param name: can be ignored, not needed
		:return: projected longitude and latitude on Earth's surface
		"""
		tle_rec = ephem.readtle(name, self.l1, self.l2)
		year, month, day, hour, minutes, sec = self.orbital_time
		time = datetime(year, month, day, hour, minutes, sec)
		tle_rec.compute(time)
		lati = (tle_rec.sublat / degree)
		longi = (tle_rec.sublong / degree)


		return lati, longi

	def move_in_orbit(self, seconds):
		"""
		This function move the satellite in its orbit
		:param seconds: how many second the satellite should move
		:return: the satellite's new space/orbit position
		"""

		# change orbital time attribute
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

		# return new position

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


		self.l2 = fix_checksum(''.join(map(str, l2_listed)))

		prev_pos_obj = self.sat_pos_obj
		# object orbit has changed, create new sat_pos_obj

		self.sat_pos_obj = twoline2rv(self.l1, self.l2, wgs72)

		return self.sat_pos_obj

	def height_sat(self, lati, longi):
		"""
        Returns distance from satellite object to a specific coordinate
        """

		year, month, day, hour, minutes, sec = self.orbital_time
		time = datetime(year, month, day, hour, minutes, sec)


		laser = ephem.Observer()
		tle_rec = ephem.readtle("name", self.l1, self.l2)
		tle_rec.compute(time)
		laser.lon = decdeg2dms(longi)
		laser.lat = decdeg2dms(lati)
		laser.elevation = 0
		laser.date = time

		tle_rec = ephem.readtle("SAT", self.l1, self.l2)
		tle_rec.compute(laser)

		d = tle_rec.range / 1000

		return d
