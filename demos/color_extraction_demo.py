import imutils
import cv2


bridge = cv2.imread("../demo_images/bridge.jpg")

bridge = imutils.resize(bridge, 250)


cv2.imshow("Main Photo", bridge)

extractColorInformation = imutils.extractDominantColor(bridge)
colorBar = imutils.plotColorBar(extractColorInformation)

print(extractColorInformation)
cv2.imshow("Extracted Color Bar", cv2.cvtColor(colorBar,
                                               cv2.COLOR_RGB2BGR))
cv2.waitKey(0)
