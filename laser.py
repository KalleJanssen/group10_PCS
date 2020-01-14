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
This class contains a Laser object

"""



class Laser(object):
	def __init__(self, longitude, latitude, power, beam_range, spot_size):
		self.longitude = longitude
		self.latitude = latitude
		self.power = power
		self.range = beam_range
		self.spot_size = spot_size

		
	def hit_satellite(satellite_object, duration):
		return 0


		