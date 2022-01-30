# import the necessary packages
from threading import Thread
import cv2


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

	def get(self, var1):
		return self.stream.get(var1)

	def set(self, var1, var2):
		return self.stream.set(var1, var2)

	def start(self):
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
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.grabbed, self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
