# Modified from: 
# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/

# Performance:
#    Python 2.7: 105.78   --> 131.75
#    Python 3.7:  15.36   -->  50.13

# USAGE
# python read_frames_fast.py --video videos/jurassic_park_intro.mp4

# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

def filterFrame(frame):
	frame = imutils.resize(frame, width=450)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame = np.dstack([frame, frame, frame])
	return frame

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
	help="path to input video file")
args = vars(ap.parse_args())

# start the file video stream thread and allow the buffer to
# start to fill
print("[INFO] starting video file thread...")
fvs = FileVideoStream(args["video"], transform=filterFrame).start()
time.sleep(1.0)

# start the FPS timer
fps = FPS().start()

# loop over frames from the video file stream
while fvs.running():
	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale (while still retaining 3
	# channels)
	frame = fvs.read()

	# Relocated filtering into producer thread with transform=filterFrame
	#  Python 2.7: FPS 92.11 -> 131.36
	#  Python 3.7: FPS 41.44 -> 50.11
	#frame = filterFrame(frame)

	# display the size of the queue on the frame
	cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
		(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)	

	# show the frame and update the FPS counter
	cv2.imshow("Frame", frame)

	cv2.waitKey(1)
	if fvs.Q.qsize() < 2:  # If we are low on frames, give time to producer
		time.sleep(0.001)  # Ensures producer runs now, so 2 is sufficient
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()