import cv2

class DENSE:
    def __init__(self, step=6, radius=.5):
        self.step = step
        self.radius = radius

    def detect(self, img):
        # initialize our list of keypoints
        kps = []

        # loop over the height and with of the image, taking a `step`
        # in each direction
        for x in range(0, img.shape[1], self.step):
            for y in range(0, img.shape[0], self.step):
                # create a keypoint and add it to the keypoints list
                kps.append(cv2.KeyPoint(x, y, self.radius))

        # return the dense keypoints
        return kps

    def setInt(self, var, val):
        if var == "initXyStep":
            self.step = val
