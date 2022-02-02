# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# BE SURE TO INSTALL 'imutils' PRIOR TO EXECUTING THIS COMMAND
# Install and start IP Camera on android, Play Store Link : https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en_IN
# python ipcamera_fps_demo.py --ip-camera-addr http://192.168.43.1:8080/video
# python ipcamera_fps_demo.py --display 1 --ip-camera-addr http://192.168.43.1:8080/video 
# REPLACE THE IP ADDRESS WITH IP ADDRESS OF YOUR SMARTPHONE. 

# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be0 displayed")
ap.add_argument("-i","--ip-camera-addr", required=True, 
	help="full address of the ip camera, eg : http://192.168.43.1:8080/video")
args = vars(ap.parse_args())

# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(args["ip_camera_addr"])

# try to read a frame and verify proper connection to Ip Camera
ret,frame = stream.read()

if ret == False:
	print('Failed to read from IP Camera with address {}.\n Check if IP camera is running and address given is correct'.format(args["ip_camera_addr"]))
	exit()

fps = FPS().start()

# loop over some frames
while fps._numFrames < args["num_frames"]:
	# grab the frame from the stream and resize it to have a maximum
	# width of 400 pixels
	(grabbed, frame) = stream.read()
	frame = imutils.resize(frame, width=400)

	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()

# created a *threaded *video stream, allow the camera senor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = VideoStream(src=args["ip_camera_addr"]).start()
fps = FPS().start()

# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()