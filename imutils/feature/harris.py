import cv2
import numpy as np
from .helpers import corners_to_keypoints


class HARRIS:
    def __init__(self, blockSize=2, apertureSize=3, k=0.1, T=0.02):
        self.blockSize = blockSize
        self.apertureSize = apertureSize
        self.k = k
        self.T = T

    def detect(self, img):
        # convert our input image to a floating point data type and then
        # compute the Harris corner matrix
        gray = np.float32(img)
        H = cv2.cornerHarris(gray, self.blockSize, self.apertureSize, self.k)

        # for every (x, y)-coordinate where the Harris value is above the
        # threshold, create a keypoint (the Harris detector returns
        # keypoint size a 3-pixel radius)
        kps = np.argwhere(H > self.T * H.max())
        kps = [cv2.KeyPoint(pt[1], pt[0], 3) for pt in kps]

        # return the Harris keypoints
        return kps
