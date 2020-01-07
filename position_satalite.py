# pip install sgp4
# https://pypi.org/project/sgp4/

from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

line1 = ('1    11U 59001A   20007.28001219  .00000298  00000-0  16445-3 0  9991')
line2 = ('2    11  32.8680 304.2915 1467991  55.9767 317.1689 11.85651085597478')

satellite = twoline2rv(line1, line2, wgs72)
position, velocity = satellite.propagate(2000, 6, 29, 12, 50, 19) # 12:50:19 on 29 June 2000n

print(satellite.error)    # nonzero on error
print(satellite.error_message)

print(position)
print(velocity)
