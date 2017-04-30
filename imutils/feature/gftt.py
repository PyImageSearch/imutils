import cv2
from .helpers import corners_to_keypoints


class GFTT:
    def __init__(self, maxCorners=0, qualityLevel=0.01, minDistance=1,
                 mask=None, blockSize=3, useHarrisDetector=False, k=0.04):
        self.maxCorners = maxCorners
        self.qualityLevel = qualityLevel
        self.minDistance = minDistance
        self.mask = mask
        self.blockSize = blockSize
        self.useHarrisDetector = useHarrisDetector
        self.k = k

    def detect(self, img):
        cnrs = cv2.goodFeaturesToTrack(img, self.maxCorners, self.qualityLevel, self.minDistance,
                                       mask=self.mask, blockSize=self.blockSize,
                                       useHarrisDetector=self.useHarrisDetector, k=self.k)

        return corners_to_keypoints(cnrs)

