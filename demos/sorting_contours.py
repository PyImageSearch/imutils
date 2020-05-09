# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# BE SURE TO INSTALL 'imutils' PRIOR TO EXECUTING THIS COMMAND
# python sorting_contours.py

# import the necessary packages
from imutils import contours
import imutils
import cv2

# load the shapes image clone it, convert it to grayscale, and
# detect edges in the image
image = cv2.imread("../demo_images/shapes.png")
orig = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = imutils.auto_canny(gray)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the (unsorted) contours and label them
for (i, c) in enumerate(cnts):
	orig = contours.label_contour(orig, c, i, color=(240, 0, 159))

# show the original image
cv2.imshow("Original", orig)

# loop over the sorting methods
for method in ("left-to-right", "right-to-left", "top-to-bottom", "bottom-to-top"):
	# sort the contours
	(cnts, boundingBoxes) = contours.sort_contours(cnts, method=method)
	clone = image.copy()

	# loop over the sorted contours and label them
	for (i, c) in enumerate(cnts):
		sortedImage = contours.label_contour(clone, c, i, color=(240, 0, 159))

	# show the sorted contour image
	cv2.imshow(method, sortedImage)

# wait for a keypress
cv2.waitKey(0)
