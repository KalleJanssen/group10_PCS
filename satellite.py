"""
This Class contains a satellite object, with its positions and spatial sctructure

NOTE: The in the TLE-file stated orbital angles and other complex space numbers will be added

"""


class Satellite(object):
	def __init__(self, x_pos, y_pos, z_pos, height, width, length, mass, cross_section):
		self.x = x_pos
		self.y = y_pos
		self.z = z_pos
		self.height = height
		self.width = width
		self.length = length
		self.mass = mass
		self.cross_section = cross_section

	def changeDirection(margin):
		return 0

		



