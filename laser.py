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
from copy import deepcopy

"""
This class contains a Laser object

"""

class Laser(object):
	def __init__(self, latitude, longitude, spot, Cm, fluence):
		"""
		:param latitude: position
		:param longitude: position
		:param range: 'danger area' for satellite
		:param Cm: is defined as the ratio of impulse density in N/W
		:param fluence: optical energy in J/cm2
		"""
		self.long = longitude
		self.lat = latitude
		self.spot = spot
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

		prev_SAT = deepcopy(satellite)

		deltaRPD = self.calc_velocity_change(satellite, duration)[0]
		print("rpd change;", deltaRPD)
		satellite.change_mean_motion(deltaRPD)





		return prev_SAT


		