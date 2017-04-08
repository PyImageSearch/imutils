# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# USAGE
# python feature_demo.py

# import the necessary packages
from imutils.feature import DescriptorExtractor_create
from imutils.feature import FeatureDetector_create
from imutils.feature import corners_to_keypoints

# ensure the keypoint detection and local invariant descriptors are
# working properly
detector = FeatureDetector_create("SIFT")
extractor = DescriptorExtractor_create("SIFT")
print(detector)
print(extractor)
print(corners_to_keypoints)