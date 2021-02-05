""" HeatBench GUI class definition """

import os
from tkinter import *
from tkinter import ttk
from queue import Queue
from hb_graph import Graph
from hb_thread import Thread_hb
from hb_process import Process
from hb_enum import *



""" Class definition """
class Gui(object):
	def __init__(self):
		# Initialize thread driven by GUI and Q for thread->GUI communication
		self._thread_meas = None
		self._queue = Queue(maxsize=10)
		self._samp_period = 0.5
		self._temp_pain = 35
		self._temp_burn = 50
		self._sensor_dir = "/home/pi/heatbench/sensors"
		self._log_dir = "/home/pi/heatbench/data"

		# Create master window
		self._win = Tk()
		self._win.title('Heat Bench')
		self._win.geometry("1400x640")

		# Create slave items
		self._label_sensor = Label(self._win, text='Sensor selection', foreground='blue')
		self._label_sensor.place(x=20, y=80)

		self._list_sensor = ttk.Combobox(self._win, values=self._get_sensor_list(), height=4, width=35)
		self._list_sensor.place(x=20, y=100)
		self._list_sensor.current(0)

		self._num_ref = Label(self._win, text='Ref = - deg', foreground='green')
		self._num_ref.place(x=20, y=150)

		self._num_sensor = Label(self._win, text='Sensor = - deg', foreground='blue')
		self._num_sensor.place(x=20, y=180)

		self._num_lim = Label(self._win, text='Pain threshold = {0} deg'.format(self._temp_pain), foreground='yellow')
		self._num_lim.place(x=20, y=210)

		self._num_lim = Label(self._win, text='Burn threshold = {0} deg'.format(self._temp_burn), foreground='red')
		self._num_lim.place(x=20, y=240)

		self._butt_start = Button(self._win, text='START', foreground='green', height=4, width=30, command=self._start_process)
		self._butt_start.place(x=20, y=350)

		self._butt_stop = Button(self._win, text='STOP', foreground='red', height=4, width=30, command=self._stop_process)
		self._butt_stop.place(x=20, y=450)
		self._butt_stop["state"] = 'disable'

		self._info_state = Label(self._win, text='')
		self._info_state.place(x=20, y=550)

		self._graph = Graph(self._win, h=600, w=1000)
		self._graph.place(x=380, y=20)

		# Run graph update function
		self._graph.animate(int(1000 * self._samp_period))

		# Run GUI update function
		self._win.after(1000, self._update_gui)

		# Run event handler
		self._win.mainloop()

	def _start_process(self):
		self._graph.clear()
		self._thread_meas = Thread_hb( Process( self._queue, self._samp_period, self._sensor_dir, self._list_sensor.get(), self._log_dir ) )
		self._thread_meas.start()
		self._list_sensor["state"] = 'disable'
		self._butt_start["state"] = 'disable'
		self._butt_stop["state"] = 'normal'

	def _stop_process(self):
		self._action_stop()

	def _update_gui(self):
		while not self._queue.empty():
			item = self._queue.get()
			if item[Msg.ID] == Id.INFO:
				self._info_state["text"] = item[Msg.DATA]
			elif item[Msg.ID] == Id.TEMP:
				self._num_ref["text"] = 'Ref = %.1f deg' % item[Msg.DATA][Temp.REF]
				self._num_sensor["text"] = 'Sensor = %.1f deg' % item[Msg.DATA][Temp.SENSOR]
				self._graph.add_point(item[Msg.DATA], self._temp_pain, self._temp_burn)
			else: # Error
				self._action_stop()
		self._win.after(100, self._update_gui)

	def _action_stop(self):
		self._thread_meas.join()
		self._thread_meas = None
		self._list_sensor["state"] = 'normal'
		self._butt_start["state"] = 'normal'
		self._butt_stop["state"] = 'disable'

	def _get_sensor_list(self):
		sensor_list = []
		for file in [ f for f in os.listdir(self._sensor_dir) if os.path.isfile(os.path.join(self._sensor_dir, f)) and f.endswith('.txt') ]:
			sensor_list.append(file.replace('.txt', ''))
		sensor_list.sort()
		return sensor_list



