# import the necessary packages
from __future__ import absolute_import
import numpy as np
import cv2
from ..convenience import is_cv2

class RootSIFT:
	def __init__(self):
		# initialize the SIFT feature extractor for OpenCV 2.4
		if is_cv2():
			self.extractor = cv2.DescriptorExtractor_create("SIFT")

		# otherwise initialize the SIFT feature extractor for OpenCV 3+
		else:
			self.extractor = cv2.xfeatures2d.SIFT_create()

	def compute(self, image, kps, eps=1e-7):
		# compute SIFT descriptors
		(kps, descs) = self.extractor.compute(image, kps)

		# if there are no keypoints or descriptors, return an empty tuple
		if len(kps) == 0:
			return ([], None)

		# apply the Hellinger kernel by first L1-normalizing and taking the
		# square-root
		descs /= (descs.sum(axis=1, keepdims=True) + eps)
		descs = np.sqrt(descs)

		# return a tuple of the keypoints and descriptors
		return (kps, descs)