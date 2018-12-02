# author:    Tim Poulsen
# website:   https://www.timpoulsen.com

# USAGE
# from the demos folder:
# python demos/contrast_demo.py -i demo_images/bridge.jpg -b 100
# python demos/contrast_demo.py -i demo_images/bridge.jpg --c 50

# import the necessary packages
from __future__ import print_function
import argparse
import cv2
import os
from imutils import adjust_brightness_contrast

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument('-b', '--brightness', default=0,
                help='Brightness, negative is darker, positive is brighter')
ap.add_argument('-c', '--contrast', default=0,
                help='Contrast, positive value for more contrast')
args = vars(ap.parse_args())
brightness = float(args['brightness'])
contrast = float(args['contrast'])
file_name = os.path.abspath(args['image'])
if os.path.isfile(file_name) is False:
    print(file_name)
    print('Cannot open image, quitting...')
    exit()

image = cv2.imread(file_name)

cv2.namedWindow('Original')
cv2.namedWindow('Adjusted')
adjusted = adjust_brightness_contrast(image, contrast=contrast, brightness=brightness)
cv2.imshow('Original', image)
cv2.imshow('Adjusted', adjusted)
cv2.waitKey(0)
