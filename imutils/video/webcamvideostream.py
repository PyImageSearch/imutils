# import the necessary packages
from threading import Thread
import cv2

class WebcamVideoStream:
	def __init__(self, src=0, name="WebcamVideoStream"):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		
		# Keep track of the source of the video capture.
		# This way, when the user calls stop() we can release the camera.
		# If the user calls start later, we can simply re-open the video capture.
		self.src = src

		(self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# If the stream was closed, re-open it before starting the update thread.
		if self.isOpened() is False:
			self.stream = cv2.VideoCapture(self.src)
			self.stopped=False
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				# When the user stops the camera, we should release the resource:
				self.stream.release()
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

	def isOpened(self):
		# Returns true if the video capture stream was successfully opened. Returns false otherwise.
		return self.stream.isOpened()
