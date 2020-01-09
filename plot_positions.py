import data_processing
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from data_processing import tle_to_positions

position_list = tle_to_positions("tle.txt")[2]
xline = [i[0] for i in position_list]
yline = [i[1] for i in position_list]
zline = [i[2] for i in position_list]
for i in range(len(xline)):
	ax = plt.axes(projection='3d')
	ax.scatter(xline[i], yline[i], zline[i], 'gray')

plt.savefig('pos.png')