# import the necessary packages
from threading import Thread
import sys
import cv2
import time

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
	from queue import Queue

# otherwise, import the Queue class for Python 2.7
else:
	from Queue import Queue

class FileVideoStream:
	def __init__(self, path, transform=None, queueSize=128):
		# initialize the file video stream along with the boolean
		# used to indicate if the thread should be stopped or not
		self.stream = cv2.VideoCapture(path)
		self.stopped = False
		self.transform = transform

		# initialize the queue used to store frames read from
		# the video file
		self.Q = Queue(maxsize=queueSize)

	def start(self):
		# start a thread to read frames from the file video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely
		while True:
			# if the thread indicator variable is set, stop the
			# thread
			if self.stopped:
				return

			# otherwise, ensure the queue has room in it
			if not self.Q.full():
				# read the next frame from the file
				(grabbed, frame) = self.stream.read()

				# if the `grabbed` boolean is `False`, then we have
				# reached the end of the video file
				if not grabbed:
					self.stop()
					return

				# if there are transforms to be done, might as well
				# do them on producer thread before handing back to
				# consumer thread. ie. Usually the producer is so far
				# ahead of consumer that we have time to spare.
				#
				# Python is not parallel but the transform operations
				# are usually OpenCV native so release the GIL.
				#
				# Really just trying to avoid spinning up additional
				# native threads and overheads of additional 
				# producer/consumer queues since this one was generally
				# idle grabbing frames.
				if self.transform:
					frame = self.transform(frame)

				# add the frame to the queue
				self.Q.put(frame)
			else:
				time.sleep(0.1)  # Rest for 10ms, we have a full queue  

	def read(self):
		# return next frame in the queue
		return self.Q.get()

	# Insufficient to have consumer use while(more()) which does
	# not take into account if the producer has reached end of
	# file stream. 
	def running(self):
		return self.more() or not self.stopped

	def more(self):
		# return True if there are still frames in the queue
		return self.Q.qsize() > 0

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True