# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# BE SURE TO INSTALL 'imutils' PRIOR TO EXECUTING THIS COMMAND
# python image_basics.py

# import the necessary packages
import matplotlib.pyplot as plt
import imutils
import cv2

# load the example images
bridge = cv2.imread("../demo_images/bridge.jpg")
cactus = cv2.imread("../demo_images/cactus.jpg")
logo = cv2.imread("../demo_images/pyimagesearch_logo.jpg")
workspace = cv2.imread("../demo_images/workspace.jpg")

# 1. TRANSLATION
# show the original image
cv2.imshow("Original", workspace)

# translate the image x-50 pixels to the left and y=100 pixels down
translated = imutils.translate(workspace, -50, 100)
cv2.imshow("Translated", translated)
cv2.waitKey(0)

# translate the image x=25 pixels to the right and y=75 pixels up
translated = imutils.translate(workspace, 25, -75)
cv2.imshow("Translated", translated)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 2. ROTATION
# loop over the angles to rotate the image
for angle in range(0, 360, 90):
    # rotate the image and display it
    rotated = imutils.rotate(bridge, angle=angle)
    cv2.imshow("Angle=%d" % (angle), rotated)

# wait for a keypress, then close all the windows
cv2.waitKey(0)
cv2.destroyAllWindows()

# 3. RESIZING
# loop over varying widths to resize the image to
for width in (400, 300, 200, 100):
    # resize the image and display it
    resized = imutils.resize(workspace, width=width)
    cv2.imshow("Width=%dpx" % (width), resized)

# wait for a keypress, then close all the windows
cv2.waitKey(0)
cv2.destroyAllWindows()

# 4. SKELETONIZATION
# skeletonize the image using a 3x3 kernel
cv2.imshow("Original", logo)
gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
skeleton = imutils.skeletonize(gray, size=(3, 3))
cv2.imshow("Skeleton", skeleton)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 5. MATPLOTLIB
# INCORRECT: show the image without converting color spaces
plt.figure("Incorrect")
plt.imshow(cactus)

# CORRECT: convert color spaces before using plt.imshow
plt.figure("Correct")
plt.imshow(imutils.opencv2matplotlib(cactus))
plt.show()

# 6. URL TO IMAGE
# load an image from a URL, convert it to OpenCV, format, and
# display it
url = "http://pyimagesearch.com/static/pyimagesearch_logo_github.png"
logo = imutils.url_to_image(url)
cv2.imshow("URL to Image", logo)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 7. AUTO CANNY
# convert the logo to grayscale and automatically detect edges
gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
edgeMap = imutils.auto_canny(gray)
cv2.imshow("Original", logo)
cv2.imshow("Automatic Edge Map", edgeMap)
cv2.waitKey(0)
