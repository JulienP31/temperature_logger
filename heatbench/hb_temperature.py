""" HeatBench temperature class definition """

import numpy as np
import time
from ads1118 import ADS1118 as ads
from hb_enum import Sensor



""" Class definition """
class Temperature(object):
	def __init__(self, ref_type, ref_coeffs, sensor_type, sensor_coeffs):
		self._R0 = 10000.0 #< Reference resistor for TH measurement -> To be measured with ohm-meter for each bench !
		self._Vdd = 3.3 #< Reference voltage
		self._ref_type = ref_type
		self._ref_coeffs = ref_coeffs if (ref_type == Sensor.THERMOCOUPLE) else self._TH_reorder_coeffs(ref_coeffs)
		self._sensor_type = sensor_type
		self._sensor_coeffs = sensor_coeffs if (sensor_type == Sensor.THERMOCOUPLE) else self._TH_reorder_coeffs(sensor_coeffs)
		self._adc = ads(0,0, 1000000, 0b01)

	def read(self):
		C_int, V_adc_ref, V_adc_sensor = self._read_data()
		temp_ref = self._TC_get_temp(V_adc_ref, C_int, self._ref_coeffs) if (self._ref_type == Sensor.THERMOCOUPLE) else self._TH_get_temp(V_adc_ref, self._ref_coeffs)
		temp_sensor = self._TC_get_temp(V_adc_sensor, C_int, self._sensor_coeffs) if (self._sensor_type == Sensor.THERMOCOUPLE) else self._TH_get_temp(V_adc_sensor, self._sensor_coeffs)
		return (temp_ref, temp_sensor)

	def _TC_Cint_to_mV(self, C_int, coeffs):
		return np.interp(C_int, coeffs[1], coeffs[0])

	def _TC_mV_to_C(self, mV, coeffs):
		return np.interp(mV, coeffs[0], coeffs[1])

	def _TC_get_temp(self, V_adc, C_int, coeffs):
		return self._TC_mV_to_C( 1000.0 * V_adc + self._TC_Cint_to_mV(C_int, coeffs), coeffs )

	def _TH_Ohm_to_C(self, Ohm, coeffs):
		return np.interp(Ohm, coeffs[0], coeffs[1])

	def _TH_get_temp(self, V_adc, coeffs):
		return self._TH_Ohm_to_C( self._R0 * V_adc / (self._Vdd - V_adc), coeffs )

	def _TH_reorder_coeffs(self, coeffs):
		coeffs_x = coeffs[0]
		coeffs_y = coeffs[1]
		if np.all(np.diff(coeffs_x) < 0): #< NTC
			coeffs_x.reverse()
			coeffs_y.reverse()
		return (coeffs_x, coeffs_y)

	def _read_data(self):
		C_int = self._read_adc(ads.MUX_AIN2_AIN3, ads.PGA_0_512V, ads.TS_MODE_TEMP)
		V_adc_ref = self._read_adc(ads.MUX_AIN2_AIN3, ads.PGA_0_512V, ads.TS_MODE_ADC)
		V_adc_sensor = self._read_adc(ads.MUX_AIN0_AIN1, ads.PGA_0_512V, ads.TS_MODE_ADC)
		return (C_int, V_adc_ref, V_adc_sensor)

	def _read_adc(self, mux=ads.MUX_AIN2_AIN3, pga=ads.PGA_0_512V, tsMode=ads.TS_MODE_TEMP):
		nb_pnt = 5
		res = 0.0
		for i in range(1 + nb_pnt): #< First ADC conversion makes data valid at second reading
			data = self._adc.readData(True, mux, pga, ads.MODE_SINGLESHOT, ads.DATARATE_128_SPS, tsMode, True, False)
			time.sleep(0.010)
			if i > 0:
				res += data			
		return (res / nb_pnt)

	def shutdown(self):
		self._adc.shutdown()



