# import the necessary packages
import numpy as np
import cv2
from ..convenience import is_cv2
from . import factories

class RootSIFT:
	def __init__(self):
		# initialize the SIFT feature extractor
		self.extractor = factories.DescriptorExtractor_create("SIFT")

	def compute(self, image, kps, eps=1e-7):
		# compute SIFT descriptors for OpenCV 2.4
		if is_cv2:
			(kps, descs) = self.extractor.compute(image, kps)

		# otherwise, computer SIFT descriptors for OpenCV 3+
		else:
			(kps, descs) = self.extractor.detectAndCompute(image, None)

		# if there are no keypoints or descriptors, return an empty tuple
		if len(kps) == 0:
			return ([], None)

		# apply the Hellinger kernel by first L1-normalizing and taking the
		# square-root
		descs /= (descs.sum(axis=1, keepdims=True) + eps)
		descs = np.sqrt(descs)

		# return a tuple of the keypoints and descriptors
		return (kps, descs)