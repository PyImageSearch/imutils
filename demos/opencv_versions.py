# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# import the necessary packages
from __future__ import print_function
import imutils
import cv2

# print the current OpenCV version on your system
print("Your OpenCV version: {}".format(cv2.__version__))

# check to see if you are using OpenCV 2.X
print("Are you using OpenCV 2.X? {}".format(imutils.is_cv2()))

# check to see if you are using OpenCV 3.X
print("Are you using OpenCV 3.X? {}".format(imutils.is_cv3(or_better=False)))

# check to see if you are using OpenCV 4.X
print("Are you using OpenCV 4.X? {}".format(imutils.is_cv4(or_better=False)))

# check to see if you are using *at least* OpenCV 2.X
print("Are you using at least OpenCV 2.X? {}".format(imutils.is_cv2(or_better=True)))

# check to see if you are using *at least* OpenCV 3.X
print("Are you using at least OpenCV 3.X? {}".format(imutils.is_cv3(or_better=True)))

# check to see if you are using *at least* OpenCV 4.X
print("Are you using at least OpenCV 4.X? {}".format(imutils.is_cv4(or_better=False)))

# should throw a deprecation warning
print("Checking for OpenCV 3: {}".format(imutils.check_opencv_version("3")))