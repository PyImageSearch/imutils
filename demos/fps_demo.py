# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# BE SURE TO INSTALL 'imutils' PRIOR TO EXECUTING THIS COMMAND
# python fps_demo.py

# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2

# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(0)
fps = FPS().start()

# loop over some frames
while fps._numFrames < 100:
	# grab the frame from the stream, resize it to have a maximum
	# width of 400 pixels, and update the FPS counter
	(grabbed, frame) = stream.read()
	frame = imutils.resize(frame, width=400)
	cv2.imshow("Frame", frame)
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()

# created a *threaded *video stream and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = VideoStream(src=0)
fps = FPS().start()

# loop over some frames...this time using the threaded stream
while fps._numFrames < 100:
	(grabbed, frame) = vs.read()
	frame = imutils.resize(frame, width=400)
	cv2.imshow("Threaded Frame", frame)
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()