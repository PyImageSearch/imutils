# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# python finding_function_names.py

# import the necessary packages
from __future__ import print_function
import imutils

# loop over various function strings to search for and try to
# locate them in the OpenCV library
for funcName in ("contour", "box", "gaussian"):
	print("[INFO] Finding all functions that contain `{}`".format(funcName))
	imutils.find_function(funcName)
	print("")