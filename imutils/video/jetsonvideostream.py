# import the necessary packages
from threading import Thread
import cv2




# Raspberry Pi Camera V2:
# Full resolution: (3280, 2646), FOV: 62.2 deg H, 48.8 deg V
# GStreamer supported full resolution: (3264, 2464), 21 FPS, FOV: 62 deg H, 48.8 deg V
# Preferred resolution: (3264,1848), 28FPS, FOV: 62 deg H, 37 deg V
class JetsonVideoStream:
	def __init__(self, captureResolution=(3264,1848), outputResolution=(960, 460), frameRate=28, flipMethod=0, 
						exposureTimeInMiliseconds=None, gain=None, digitalGain=None, whiteBalanceMode=1,
						name="JetsonVideoStream"):
		# set up the gstreamer string used to set up the camera on the jetson board
		# exposureTime - in miliseconds (0.013 to 683)
		# gain ( 1.000000 to 10.625000)
		captureWidth, captureHeight = captureResolution
		width, height = outputResolution
		
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

		whiteBalanceModeString = 'wbmode=%d ' % whiteBalanceMode if whiteBalanceMode is not 1 else ''  # 0 - auto (?)
        
		cameraString =	('nvarguscamerasrc %s%s%s! '
               			'video/x-raw(memory:NVMM), '
               			'width=(int)%d, height=(int)%d, '
               			'format=(string)NV12, framerate=(fraction)%d/1 ! '
               			'nvvidconv flip-method=%d ! '
               			'video/x-raw, width=(int)%d, height=(int)%d, '
               			'format=(string)BGRx ! '
               			'videoconvert ! video/x-raw, format=(string)BGR! appsink ' # OR format=(string)I420 
						'wait-on-eos=false drop=true max-buffers=1' 
						# 'wait-on-eos=false drop=true max-buffers=1 -e -vvv'
						 % (whiteBalanceModeString, gainString, exposureTimeString,
						 captureWidth, captureHeight, frameRate, flipMethod, width, height) )
		
		print ('OpenCV Gstreamer pipeline input string: \n', cameraString)

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


# nvarguscamerasrc parameters description
'''
jetson@jetson-desktop:~$ gst-inspect-1.0 nvarguscamerasrc
Factory Details:
  Rank                     primary (256)
  Long-name                NvArgusCameraSrc
  Klass                    Video/Capture
  Description              nVidia ARGUS Camera Source
  Author                   Viranjan Pagar <vpagar@nvidia.com>, Amit Pandya <apandya@nvidia.com>

Plugin Details:
  Name                     nvarguscamerasrc
  Description              nVidia ARGUS Source Component
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstnvarguscamerasrc.so
  Version                  1.0.0
  License                  Proprietary
  Source module            nvarguscamerasrc
  Binary package           NvARGUSCameraSrc
  Origin URL               http://nvidia.com/

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBaseSrc
                         +----GstNvArgusCameraSrc

Pad Templates:
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-raw(memory:NVMM)
                  width: [ 1, 2147483647 ]
                 height: [ 1, 2147483647 ]
                 format: { (string)NV12 }
              framerate: [ 0/1, 120/1 ]

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SRC: 'src'
    Pad Template: 'src'

Element Properties:
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "nvarguscamerasrc0"
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  blocksize           : Size in bytes to read per buffer (-1 = default)
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 4294967295 Default: 4096 
  num-buffers         : Number of buffers to output before sending EOS (-1 = unlimited)
                        flags: readable, writable
                        Integer. Range: -1 - 2147483647 Default: -1 
  typefind            : Run typefind before negotiating (deprecated, non-functional)
                        flags: readable, writable, deprecated
                        Boolean. Default: false
  do-timestamp        : Apply current stream time to buffers
                        flags: readable, writable
                        Boolean. Default: true
  silent              : Produce verbose output ?
                        flags: readable, writable
                        Boolean. Default: true
  timeout             : timeout to capture in seconds (Either specify timeout or num-buffers, not both)
                        flags: readable, writable
                        Unsigned Integer. Range: 0 - 2147483647 Default: 0 
  wbmode              : White balance affects the color temperature of the photo
                        flags: readable, writable
                        Enum "GstNvArgusCamWBMode" Default: 1, "auto"
                           (0): off              - GST_NVCAM_WB_MODE_OFF
                           (1): auto             - GST_NVCAM_WB_MODE_AUTO
                           (2): incandescent     - GST_NVCAM_WB_MODE_INCANDESCENT
                           (3): fluorescent      - GST_NVCAM_WB_MODE_FLUORESCENT
                           (4): warm-fluorescent - GST_NVCAM_WB_MODE_WARM_FLUORESCENT
                           (5): daylight         - GST_NVCAM_WB_MODE_DAYLIGHT
                           (6): cloudy-daylight  - GST_NVCAM_WB_MODE_CLOUDY_DAYLIGHT
                           (7): twilight         - GST_NVCAM_WB_MODE_TWILIGHT
                           (8): shade            - GST_NVCAM_WB_MODE_SHADE
                           (9): manual           - GST_NVCAM_WB_MODE_MANUAL
  saturation          : Property to adjust saturation value
                        flags: readable, writable
                        Float. Range:               0 -               2 Default:               1 
  sensor-id           : Set the id of camera sensor to use. Default 0.
                        flags: readable, writable
                        Integer. Range: 0 - 255 Default: 0 
  exposuretimerange   : Property to adjust exposure time range in nanoseconds
			Use string with values of Exposure Time Range (low, high)
			in that order, to set the property.
			eg: exposuretimerange="34000 358733000"
                        flags: readable, writable
                        String. Default: null
  gainrange           : Property to adjust gain range
			Use string with values of Gain Time Range (low, high)
			in that order, to set the property.
			eg: gainrange="1 16"
                        flags: readable, writable
                        String. Default: null
  ispdigitalgainrange : Property to adjust digital gain range
			Use string with values of ISP Digital Gain Range (low, high)
			in that order, to set the property.
			eg: ispdigitalgainrange="1 8"
                        flags: readable, writable
                        String. Default: null
  tnr-strength        : property to adjust temporal noise reduction strength
                        flags: readable, writable
                        Float. Range:              -1 -               1 Default:              -1 
  tnr-mode            : property to select temporal noise reduction mode
                        flags: readable, writable
                        Enum "GstNvArgusCamTNRMode" Default: 1, "NoiseReduction_Fast"
                           (0): NoiseReduction_Off - GST_NVCAM_NR_OFF
                           (1): NoiseReduction_Fast - GST_NVCAM_NR_FAST
                           (2): NoiseReduction_HighQuality - GST_NVCAM_NR_HIGHQUALITY
  ee-mode             : property to select edge enhnacement mode
                        flags: readable, writable
                        Enum "GstNvArgusCamEEMode" Default: 1, "EdgeEnhancement_Fast"
                           (0): EdgeEnhancement_Off - GST_NVCAM_EE_OFF
                           (1): EdgeEnhancement_Fast - GST_NVCAM_EE_FAST
                           (2): EdgeEnhancement_HighQuality - GST_NVCAM_EE_HIGHQUALITY
  ee-strength         : property to adjust edge enhancement strength
                        flags: readable, writable
                        Float. Range:              -1 -               1 Default:              -1 
  aeantibanding       : property to set the auto exposure antibanding mode
                        flags: readable, writable
                        Enum "GstNvArgusCamAeAntiBandingMode" Default: 1, "AeAntibandingMode_Auto"
                           (0): AeAntibandingMode_Off - GST_NVCAM_AEANTIBANDING_OFF
                           (1): AeAntibandingMode_Auto - GST_NVCAM_AEANTIBANDING_AUTO
                           (2): AeAntibandingMode_50HZ - GST_NVCAM_AEANTIBANDING_50HZ
                           (3): AeAntibandingMode_60HZ - GST_NVCAM_AEANTIBANDING_60HZ
  exposurecompensation: property to adjust exposure compensation
                        flags: readable, writable
                        Float. Range:              -2 -               2 Default:               0 
  aelock              : set or unset the auto exposure lock
                        flags: readable, writable
                        Boolean. Default: false
  awblock             : set or unset the auto white balance lock
                        flags: readable, writable
                        Boolean. Default: false
  maxperf             : set or unset the max performace
                        flags: readable, writable
                        Boolean. Default: false
  bufapi-version      : set to use new Buffer API
                        flags: readable, writable
                        Boolean. Default: false



'''