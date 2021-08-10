# import the necessary packages
from .webcamvideostream import WebcamVideoStream

class VideoStream:
	def __init__(self, src=0, usePiCamera=False, resolution=(320, 240),
		framerate=32, **kwargs):
		# check to see if the picamera module should be used
		if usePiCamera:
			# only import the picamera packages unless we are
			# explicity told to do so -- this helps remove the
			# requirement of `picamera[array]` from desktops or
			# laptops that still want to use the `imutils` package
			from .pivideostream import PiVideoStream

			# initialize the picamera stream and allow the camera
			# sensor to warmup
			self.stream = PiVideoStream(resolution=resolution,
				framerate=framerate, **kwargs)

		# otherwise, we are using OpenCV so initialize the webcam
		# stream
		else:
			self.stream = WebcamVideoStream(src=src)

	def start(self):
		# start the threaded video stream
		return self.stream.start()

	def update(self):
		# grab the next frame from the stream
		self.stream.update()

	def read(self):
		# return the current frame
		return self.stream.read()

	def stop(self):
		# stop the thread and release any resources
		self.stream.stop()

	def set_video_setting(self, setting_to_change, set_value):
		if not usePiCamera:
			self.stream.set_video_setting(setting_to_change, set_value)

	def get_video_setting(self, setting_to_check):
		if not usePiCamera:
			return self.stream.get(setting_to_check)
