""" HeatBench datalog class definition """

from datetime import datetime
from hb_enum import Temp



""" Class definition """
class DataLog(object):
	def __init__(self, filedir, sensor):
		self._filepath = "%s/%s_%s.csv" % (filedir, sensor, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
		self._file = None

	def create(self):
		self._file = open(self._filepath, "w")
		self._file.write("Time [s],Ref temp [deg C],Sensor temp [deg C]\n")		

	def write(self, data):
		self._file.write("%.2f,%.2f,%.2f\n" % data)

	def close(self):
		if self._file:
			self._file.close()



