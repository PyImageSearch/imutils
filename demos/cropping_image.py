# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# BE SURE TO INSTALL 'imutils' PRIOR TO EXECUTING THIS COMMAND
# python image_basics.py

import imutils
import cv2

# Load the example image
image = cv2.imread("../demo_images/shapes.png")

# Crop the image by using mouse click
cropped = imutils.click_and_crop(image)

# Show the original and cropped one
cv2.imshow("Original", image)
cv2.imshow("Cropped", cropped)

# Wait for a keypress, then close all the windows
cv2.waitKey(0)
cv2.destroyAllWindows()
