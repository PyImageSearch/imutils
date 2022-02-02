# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import time

class PiVideoStream:
	def __init__(self, resolution=(320, 240), framerate=32, **kwargs):
		# initialize the camera
		self.camera = PiCamera()

		# set camera parameters
		self.camera.resolution = resolution
		self.camera.framerate = framerate

		# set optional camera parameters (refer to PiCamera docs)
		for (arg, value) in kwargs.items():
			setattr(self.camera, arg, value)

		# initialize the stream
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)

		# initialize the frame and the checker that checks is it updated
		# and the variable used to indicate if the thread should be stopped
		self.frame = None
		self.is_updated = False
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame and update the update checker
			self.frame = f.array
			self.rawCapture.truncate(0)
			self.is_updated = True

			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return

	def read(self):
		# block until there is newly updated frame
		while not self.is_updated:
			if self.stopped:
				return None
			time.sleep(0.001)
			continue
		self.is_updated = False
		# return the newly updated frame
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

