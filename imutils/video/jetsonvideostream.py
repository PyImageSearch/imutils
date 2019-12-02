# import the necessary packages
from threading import Thread
import cv2

class JetsonVideoStream:
	def __init__(self, outputResolution=(960, 40), frameRate=28, flipMethod=0, exposureTimeInMiliseconds=None, gain=None, name="JetsonVideoStream"):
		# set up the gstreamer string used to set up the camera on 
		# the jetson board
		# exposureTime - in miliseconds (0,013 to 683)
		# gain ( 1.000000 to 10.625000)

		width = outputResolution[0]
		height = outputResolution[1]
		exposureTimeSting = ''
		gainString = ''
		if exposureTimeInMiliseconds is not None:
			toNanoseconds = exposureTimeInMiliseconds * 1000000
			exposureTimeSting = ' exposuretimerange="{}" "{}"'.format(toNanoseconds, toNanoseconds)
		if gain is not None:
			gainString = ' gainrange="{}" "{}"'.format(gain, gain)
		# ispdigitalgainrange - unknown parameter (digital gain), maybe important
		
		# some more options: http://www.neko.ne.jp/~freewing/raspberry_pi/nvidia_jetson_nano_setup_raspberry_pi_camera_module_v2/
		awblock = False
		aelock = False
		autoWhiteBalanceLockString = ' awblock=true' if awblock is True else ''
		autoExposureLockString = ' aelock=true' if aelock is True else ''

		whiteBalanceModeString = ' wbmode=0' # 0 - auto (?)
                       
		cameraString = ('nvarguscamerasrc{}{} ! '
               			'video/x-raw(memory:NVMM), '
               			'width=(int)3820, height=(int)1848, '
               			'format=(string)NV12, framerate=(fraction){}/1 ! '
               			'nvvidconv flip-method=(int){}  ! '
               			'video/x-raw, width=(int){}, height=(int){}, '
               			'format=(string)BGRx ! '
               			'videoconvert ! video/x-raw, format=BGR ! appsink').format(gainString, exposureTimeSting, frameRate, flipMethod, width, height)
		# Original string from pull request:
		# cameraString = ('nvcamerasrc ! '
		# 						'video/x-raw(memory:NVMM), '
		# 						'width=(int)2592, height=(int)1458, '
		# 						'format=(string)I420, framerate=(fraction)30/1 ! '
		# 						'nvvidconv ! '
		# 						'video/x-raw, width=(int){}, height=(int){}, '
		# 						'format=(string)BGRx ! '
		# 						'videoconvert ! appsink').format(width, height)

		# initialize the video camera stream using gstreamer and read 
		# the first frame from the stream
		self.stream = cv2.VideoCapture(cameraString, cv2.CAP_GSTREAMER)
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

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
				# self.stream.release() - TODO: only if it is necessary to release after stopping, can prevent resource blocking
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
