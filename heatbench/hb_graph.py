""" HeatBench graph class definition """

from tkinter import *
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from hb_enum import Temp



""" Class definition """
class Graph(Canvas):
	def __init__(self, win=None, h=100, w=100):
		super(Graph, self).__init__(win)

		style.use("ggplot")

		self._fig = Figure(figsize=(w/100, h/100))
		self._axis = self._fig.add_subplot(111)
		self.clear()

		self._canvas = FigureCanvasTkAgg(self._fig, self)
		self._canvas.get_tk_widget().pack()

	def add_point(self, point, lim1, lim2):
		self._x.append(point[Temp.TIME])
		self._y_ref.append(point[Temp.REF])
		self._y_sensor.append(point[Temp.SENSOR])
		self._y_lim1.append(lim1)
		self._y_lim2.append(lim2)
		if len(self._x) > 120:
			del self._x[0]
			del self._y_ref[0]
			del self._y_sensor[0]
			del self._y_lim1[0]
			del self._y_lim2[0]

	def clear(self, reset_data=True):
		if reset_data:
			self._x = []
			self._y_ref = []
			self._y_sensor = []
			self._y_lim1 = []
			self._y_lim2 = []
		self._axis.clear()
		self._axis.set_xlabel('Time [s]')
		self._axis.set_ylabel('Temperature [deg C]')

	def _update(self, dt):
		if self._x:
			self.clear(reset_data=False)
			self._axis.plot(self._x, self._y_ref, 'g.-')
			self._axis.plot(self._x, self._y_sensor, 'b.-')
			self._axis.plot(self._x, self._y_lim1, 'y,--')
			self._axis.plot(self._x, self._y_lim2, 'r,--')

	def animate(self, interval=1000):
		self._ani = animation.FuncAnimation(self._fig, self._update, interval)



