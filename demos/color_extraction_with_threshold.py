import imutils
import cv2
import numpy as np


def extractSkin(image):
    # Taking a copy of the image
    img = image.copy()
    # Converting from BGR Colours Space to HSV
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Defining HSV Threadholds
    lower_threshold = np.array([0, 48, 80], dtype=np.uint8)
    upper_threshold = np.array([20, 255, 255], dtype=np.uint8)

    # Single Channel mask,denoting presence of colours in the about threshold
    skinMask = cv2.inRange(img, lower_threshold, upper_threshold)

    # Cleaning up mask using Gaussian Filter
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)

    # Extracting skin from the threshold mask
    skin = cv2.bitwise_and(img, img, mask=skinMask)

    # Return the Skin image
    return cv2.cvtColor(skin, cv2.COLOR_HSV2BGR)


# Main App functions


skinImage = cv2.imread("../demo_images/skin.jpg")

skinImage = imutils.resize(skinImage, 250)

skinImage = extractSkin(skinImage)


cv2.imshow("Main Photo", skinImage)

extractColorInformation = imutils.extractDominantColor(
    skinImage, hasThresholding=True)

colorBar = imutils.plotColorBar(extractColorInformation)

print(extractColorInformation)
cv2.imshow("Extracted Color Bar", cv2.cvtColor(colorBar,
                                               cv2.COLOR_RGB2BGR))
cv2.waitKey(0)
