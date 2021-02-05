""" HeatBench enum definition """

from enum import IntEnum



class State(IntEnum):
	IDLE = 0
	INIT = 1
	WAIT_TRIG = 2
	MEAS = 3
	WAIT_SAMP = 4

class Msg(IntEnum):
	ID = 0
	DATA = 1

class Id(IntEnum):
	ERROR = 0
	INFO = 1
	TEMP = 2

class Temp(IntEnum):
	TIME = 0
	REF = 1
	SENSOR = 2

class Sensor(IntEnum):
	THERMOCOUPLE = 1
	THERMISTOR = 2 #< PTC/NTC thermistor or RTD



