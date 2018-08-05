import cv2
import imutils

class DENSE:
    def __init__(self, step=6, radius=.5):
        self.step = step
        self.radius = radius

    def detect(self, img, mask=None):

        xStart = 0
        xEnd = img.shape[1]
        yStart = 0
        yEnd = img.shape[0]

        # Mask
        if mask is not None:
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]
            peri = cv2.arcLength(cnts[0], True)
            approx = cv2.approxPolyDP(cnts[0], 0.01 * peri, True)
            (x, y, w, h) = cv2.boundingRect(approx)

            xStart = x
            xEnd = x + w
            yStart = y
            yEnd = y + h

        # initialize our list of keypoints
        kps = []

        # loop over the height and with of the image, taking a `step`
        # in each direction
        for x in range(xStart, xEnd, self.step):
            for y in range(yStart, yEnd, self.step):
                # create a keypoint and add it to the keypoints list
                kps.append(cv2.KeyPoint(x, y, self.radius))

        # return the dense keypoints
        return kps

    def setInt(self, var, val):
        if var == "initXyStep":
            self.step = val
