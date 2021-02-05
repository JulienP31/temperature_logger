""" HeatBench GPIO class definition """

import RPi.GPIO as gpio



""" Class definition """
class DigitalInput(object):
	def __init__(self):
		self._gpio = 2
		gpio.setmode(gpio.BCM)
		gpio.setup(self._gpio, gpio.IN)

	def get_state(self):
		return gpio.input(self._gpio)

	def shutdown(self):
		gpio.cleanup()



