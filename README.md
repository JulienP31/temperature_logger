# temperature_logger
Dual temperature sensor data logger [Raspberry Pi]



- Python project with GUI using Tkinter and Matplotlib : see 'GUI.png'

- 2 temperature channels :
	> Ref [GREEN] = K-type thermocouple (fixed)
	> Sensor [BLUE] = any sensor selected (thermocouple, Pt100, NTC, etc...)

- Sensor conversion tables provided in 'heatbench/sensors' directory (new tables can be created)

- NOTA : file 'ads1118.py' taken from official ads1118 lib and slightly modified
