""" HeatBench thread class definition """

import traceback
from threading import Thread, Event



""" Class definition """
class Thread_hb(Thread):
	def __init__(self, process):
		super(Thread_hb, self).__init__()
		self._process = process
		self._stoprequest = Event()

	def run(self):
		try:
			error = None
			self._process.initialize()
			while not self._stoprequest.isSet():
				self._process.run()
		except Exception as e:
			error = e
			traceback.print_exc()
			self._stoprequest.set()
		finally:
			self._process.shutdown(error)

	def join(self, timeout=None):
		self._stoprequest.set()
		super(Thread_hb, self).join(timeout)



