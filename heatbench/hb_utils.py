""" HeatBench utilities """

from hb_enum import Sensor



def read_sensor_file(file):
	sensor_id = {'TC': Sensor.THERMOCOUPLE, 'TH': Sensor.THERMISTOR}

	# Read file content
	with open(file, 'r') as csv_file:
		sensor_file_data = csv_file.readlines()

	# Get sensor type (TC or TH)
	sensor_type = sensor_id.get(sensor_file_data[0].replace('\n', ''))
	if sensor_type == None:
		raise ValueError('Invalid sensor type !')

	# Get sensor coeffs
	coeffs_x = [] #< mV (TC) or Ohm (TH)
	coeffs_y = [] #< Temp
	for line in sensor_file_data[2:]:
		y, x = line.replace('\n', '').split('\t')
		coeffs_x.append(float(x))
		coeffs_y.append(float(y))
	sensor_coeffs = (coeffs_x, coeffs_y)

	return sensor_type, sensor_coeffs



