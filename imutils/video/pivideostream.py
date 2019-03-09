# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import logging
import cv2

class PiVideoStream:
	def __init__(self, resolution=(320, 240), framerate=30,  sensor_mode = 0, logging = False, **options):
		# initialize the camera and stream
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.framerate = framerate
		self.camera.sensor_mode = sensor_mode
		for key, value in options.items():
			setattr(self.camera, key, value)
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,format="bgr", use_video_port=True)

		#thread intialization
		self.thread = None

		#enable logging
		self.logging = logging

		self.stopped = False


	def start(self):
		# start the thread to read frames from the video stream
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		try:
			for stream in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
				if stream is None:
					self.stopped =True
				if self.stopped:
					break
				self.frame = stream.array
				self.rawCapture.seek(0)
				self.rawCapture.truncate()
		except Exception as e:
			if self.logging:
				logging.error(traceback.format_exc())
			pass
		# release resource camera resources
		self.stream.close()
		self.rawCapture.close()
		self.camera.close()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		# wait until stream resources are released (producer thread might be still grabbing frame)
		if self.thread is not None: 
			self.thread.join()
			#properly handle thread exit

