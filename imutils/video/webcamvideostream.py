# import the necessary packages
from threading import Thread
import cv2

class WebcamVideoStream:
	def __init__(self, src=0, name="WebcamVideoStream"):
		# initialize the video camera stream and read the first frame
		self.src = src
		# run hidden start function
		self.__start__()
		# initialize the thread name
		self.name = name

	def __start__(self):
		"""
        start opencv stream by taking one image
        :return:
        """
		# from the stream
		self.stream = cv2.VideoCapture(self.src)
		(self.grabbed, self.frame) = self.stream.read()
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		"""
        Start streaming thread, auto-open video capture if its been stopped
        :return:
        """
		if self.stopped:
			self.__start__()
		# start the thread to read frames from the video stream
		self.t = Thread(target=self.update, name=self.name, args=())
		self.t.daemon = True
		self.t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		self.t.join()
		self.stream.release()

	def __del__(self):
		# auto release camera when deleting object:
		self.stream.release()

