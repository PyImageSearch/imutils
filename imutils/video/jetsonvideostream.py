# import the necessary packages
from threading import Thread
import cv2

class JetsonVideoStream:
	def __init__(self, outputResolution=(960, 460), frameRate=28, flipMethod=0, 
						exposureTimeInMiliseconds=None, gain=None, digitalGain=None, whiteBalanceMode=0,
						name="JetsonVideoStream"):
		# set up the gstreamer string used to set up the camera on the jetson board
		# exposureTime - in miliseconds (0.013 to 683)
		# gain ( 1.000000 to 10.625000)
		captureWidth = 3264
		captureHeight = 1848
		width = outputResolution[0]
		height = outputResolution[1]
		
		exposureTimeString = ''
		gainString = ''

		if exposureTimeInMiliseconds is not None:
			toNanoseconds = int(exposureTimeInMiliseconds * 1000000)
			exposureTimeString = 'exposuretimerange="%d %d" ' % (toNanoseconds, toNanoseconds)

		gainString = ''
		if gain is not None:
			gainString = 'gainrange="%.3f %.3f" ' % (gain, gain)

		# ispdigitalgainrange - unknown parameter (digital gain), maybe important
		
		# some more options: http://www.neko.ne.jp/~freewing/raspberry_pi/nvidia_jetson_nano_setup_raspberry_pi_camera_module_v2/
		awblock = False
		aelock = False
		autoWhiteBalanceLockString = 'awblock=true ' if awblock is True else ''
		autoExposureLockString = 'aelock=true ' if aelock is True else ''

		whiteBalanceModeString = 'wbmode=%d ' % whiteBalanceMode if whiteBalanceMode is not 0 else ''  # 0 - auto (?)
        
		cameraString =	('nvarguscamerasrc %s%s%s! '
               			'video/x-raw(memory:NVMM), '
               			'width=(int)%d, height=(int)%d, '
               			'format=(string)NV12, framerate=(fraction)%d/1 ! '
               			'nvvidconv flip-method=%d ! '
               			'video/x-raw, width=(int)%d, height=(int)%d, '
               			'format=(string)BGRx ! '
               			'videoconvert ! video/x-raw, format=(string)BGR ! appsink ' # OR format=(string)I420
						'wait-on-eos=false drop=true max-buffers=1 -e -vvv' % (whiteBalanceModeString, gainString, exposureTimeString,
																			   captureWidth, captureHeight, frameRate, flipMethod, width, height) )
		
		print (cameraString)

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
				self.stream.release() # TODO: only if it is necessary to release after stopping, can prevent resource blocking
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
