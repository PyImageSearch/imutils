# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# BE SURE TO INSTALL 'imutils' PRIOR TO EXECUTING THIS COMMAND
# python temp_file.py --image ../demo_images/bridge.jpg 

# import the necessary packages
from __future__ import print_function
from imutils.io import TempFile
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = ap.parse_args()

# load the input image
image = cv2.imread(args.image)

# create a temporary path for the image, then write the image
# to file
t = TempFile()
cv2.imwrite(t.path, image)
print("[INFO] path: {}".format(t.path))

# delete the file
t.cleanup()