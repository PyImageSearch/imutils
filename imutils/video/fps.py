# import the necessary packages
import datetime


class FPS:
	def __init__(self):
		'''Create a new FPS timer.'''
		# Store the total elapsed time and the total number of frames
		# that were examined during that elapsed time.
		# Start time and end time apply only to a given segment.
		self._elapsed = datetime.timedelta()
		self._start = None
		self._end = None
		self._numFrames = 0
		self._is_paused = False

	def start(self):
		'''Start the timer.'''
		self._start = datetime.datetime.now()
		return self

	def stop(self):
		'''Stop the timer.'''
		self._end = datetime.datetime.now()
		self._elapsed += (self._end - self._start)

	def pause(self):
		'''Pause the timer.'''
		self.stop()
		self._is_paused = True

	def resume(self):
		'''Resume the timer from a pause.'''
		self.start()
		self._is_paused = False

	def update(self):
		'''Increment the total number of frames examined during the
		timing intervals.'''
		# ignore this call while we're paused
		if not self._is_paused:
			self._numFrames += 1

	def elapsed(self):
		'''Return the total number of seconds during the
		timing intervals.'''
		return self._elapsed.total_seconds()

	def fps(self):
		'''Return the (approximate) frames per second.'''
		return self._numFrames / self.elapsed()
