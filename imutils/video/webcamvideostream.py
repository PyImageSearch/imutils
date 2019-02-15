# import the necessary packages
from threading import Thread
import cv2
import time

class WebcamVideoStream:
	def __init__(self, src=0, name="WebcamVideoStream"):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False
		self.numFrames = 0
		self.newFrame = True
		self.sleeptimes = 0

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		self.numFrames = 0
		self.sleeptimes = 0
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
			self.newFrame = True
			self.numFrames += 1

	def read(self):
		if not self.newFrame:
			while not self.newFrame and not self.stopped:
				time.sleep(0.001)
				self.sleeptimes += 1
		self.newFrame = False
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
