from satellite import Satellite
from datetime import datetime
import ephem
from copy import deepcopy

"""
------------------------------------------------------------------------------------
This class contains a Laser object that respresents the propulsion laser with it's
necessary model, attributes and functions
------------------------------------------------------------------------------------
"""

class Laser(object):
	def __init__(self, latitude, longitude, range, Cm, fluence):
		"""
		This functions initializes a laser object with it's position
		and the parameters for the beam power.
		:param latitude: position
		:param longitude: position
		:param range: range/spot of the laser in lat/long
		:param Cm: is defined as the ratio of impulse density in N/W
		:param fluence: optical energy in J/cm2
		"""
		self.long = longitude
		self.lat = latitude
		self.range = range
		self.fluence = fluence
		self.Cm = Cm




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


	def calc_velocity_change(self, satellite: Satellite, duration):
		"""
		This function calculates the velocity change (delta V) using
		a simplified physical model for a laser.
		:param satellite: satellite to calculate velocity change for
		:param duration: duration of the exposure to the laser
		:return: change of velocity in m/s, change of velocity in revolution/day
		"""

		# simplified model
		# lasering satellite for a specific duration
		deltaV = 0
		for i in range(duration):

			sat_mass = 10
			Q = self.fluence / sat_mass
			deltaV += self.Cm * Q

		# convert m/s to rpm (revolutions per minute)
		r = satellite.calc_height()[0] * 1000
		RPM = deltaV / (r * 0.10472)

		# convert RPM to relovutions per day to change mean motion
		deltaRPD = RPM * 60 * 24


		return deltaRPD, deltaV


	def hit_satellite(self, satellite: Satellite, duration):
		"""
		This function changes the mean motion of the
		satellite object using the velocity change obtained
		with calc_velocity_change. Changing the mean motion
		means it changes its orbit as well.
		:param satellite:
		:param duration:
		:return: satellite object with old orbit copied with deepcopy
		"""

		# deepcopy old object to return
		prev_SAT = deepcopy(satellite)

		# change current object's mean motion
		deltaRPD = self.calc_velocity_change(satellite, duration)[0]
		satellite.change_mean_motion(deltaRPD)

		return prev_SAT


		