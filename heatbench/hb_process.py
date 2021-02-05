""" HeatBench process class definition """

import time
from hb_gpio import DigitalInput
from hb_temperature import Temperature
from hb_datalog import DataLog
from hb_utils import read_sensor_file
from hb_enum import *



""" Class definition """
class Process(object):
	def __init__(self, queue, samp_period, sensor_dir, sensor, log_dir):
		self._queue = queue
		self._samp_period = samp_period
		self._ref_file = "{0}/{1}.txt".format(sensor_dir, 'tc_k-type_standard')
		self._sensor_file = "{0}/{1}.txt".format(sensor_dir, sensor)
		self._sensor = sensor
		self._log_dir = log_dir

		self._digital_input = None
		self._temperature = None
		self._datalog = None

		self._state = State.IDLE
		self._nb_pnt = 0
		self._time_samp = None

	def initialize(self):
		self._digital_input = DigitalInput()
		self._temperature = Temperature(*read_sensor_file(self._ref_file), *read_sensor_file(self._sensor_file))
		self._datalog = DataLog(self._log_dir, self._sensor)
		self._state = State.INIT

	def run(self):
		self._switch_state(self._state)

	def _switch_state(self, state):
		switcher = {
			State.INIT: self._action_init,
			State.WAIT_TRIG: self._action_wait_trig,
			State.MEAS: self._action_meas,
			State.WAIT_SAMP: self._action_wait_samp
		}
		action_func = switcher.get(state, self._action_error)
		action_func()

	def _action_init(self):
		self._queue.put([Id.INFO, 'Waiting for trigger...'])
		self._nb_pnt = 0
		self._state = State.WAIT_TRIG

	def _action_wait_trig(self):
		if (self._digital_input.get_state() == 0):
			self._datalog.create()
			self._time_samp = time.time()
			self._queue.put([Id.INFO, 'Running'])
			self._state = State.MEAS
		else:
			time.sleep(0.1)

	def _action_meas(self):
		data = (self._nb_pnt * self._samp_period, *self._temperature.read())
		self._datalog.write(data)
		self._queue.put([Id.TEMP, data])
		self._nb_pnt += 1
		self._state = State.WAIT_SAMP

	def _action_wait_samp(self):
		time_curr = time.time()
		if (time_curr - self._time_samp) >= self._samp_period:
			self._time_samp += self._samp_period
			self._state = State.MEAS
		else:
			time.sleep(self._samp_period/10.0)

	def _action_error(self):
		raise ValueError('Invalid process state !')

	def shutdown(self, error=None):
		if not error:
			self._queue.put([Id.INFO, 'Stopped'])
		else:
			self._queue.put([Id.INFO, 'Error !'])
			self._queue.put([Id.ERROR])
		if self._digital_input:
			self._digital_input.shutdown()
		if self._temperature:
			self._temperature.shutdown()
		if self._datalog:
			self._datalog.close()
		self._state = State.IDLE



