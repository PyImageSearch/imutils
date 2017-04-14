# import the necessary packages
from collections import OrderedDict
import numpy as np
import cv2

# define a dictionary that maps the indexes of the facial
# landmarks to specific face regions
FACIAL_LANDMARKS_IDXS = OrderedDict([
	("mouth", (48, 68)),
	("right_eyebrow", (17, 22)),
	("left_eyebrow", (22, 27)),
	("right_eye", (36, 42)),
	("left_eye", (42, 48)),
	("nose", (27, 35)),
	("jaw", (0, 17))
])

def rect_to_bb(rect):
	# take a bounding predicted by dlib and convert it
	# to the format (x, y, w, h) as we would normally do
	# with OpenCV
	x = rect.left()
	y = rect.top()
	w = rect.right() - x
	h = rect.bottom() - y

	# return a tuple of (x, y, w, h)
	return (x, y, w, h)

def shape_to_np(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((68, 2), dtype=dtype)

	# loop over the 68 facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, 68):
		coords[i] = (shape.part(i).x, shape.part(i).y)

	# return the list of (x, y)-coordinates
	return coords

def visualize_facial_landmarks(image, shape, colors=None, alpha=0.75):
	# create two copies of the input image -- one for the
	# overlay and one for the final output image
	overlay = image.copy()
	output = image.copy()

	# if the colors list is None, initialize it with a unique
	# color for each facial landmark region
	if colors is None:
		colors = [(19, 199, 109), (79, 76, 240), (230, 159, 23),
			(168, 100, 168), (158, 163, 32),
			(163, 38, 32), (180, 42, 220)]

	# loop over the facial landmark regions individually
	for (i, name) in enumerate(FACIAL_LANDMARKS_IDXS.keys()):
		# grab the (x, y)-coordinates associated with the
		# face landmark
		(j, k) = FACIAL_LANDMARKS_IDXS[name]
		pts = shape[j:k]

		# check if are supposed to draw the jawline
		if name == "jaw":
			# since the jawline is a non-enclosed facial region,
			# just draw lines between the (x, y)-coordinates
			for l in range(1, len(pts)):
				ptA = tuple(pts[l - 1])
				ptB = tuple(pts[l])
				cv2.line(overlay, ptA, ptB, colors[i], 2)

		# otherwise, compute the convex hull of the facial
		# landmark coordinates points and display it
		else:
			hull = cv2.convexHull(pts)
			cv2.drawContours(overlay, [hull], -1, colors[i], -1)

	# apply the transparent overlay
	cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

	# return the output image
	return output

def blurout_faces(image, face_rects, blur_function, *args, **kwargs):
	"""
	Blur out faces in the image given the face_rects. This function DOES NOT perform face detection. It expects
	faces rects to be given as argument.
	:param image: Image to be processed
	:param face_rects: Sequence of (x, y, w, h) of every face
	:param blur_function: One of cv2.GaussianBlur(), cv2.medianBlur(), etc...
	:param args: Args to be supplied to `blur_function`
	:param kwargs: Kwargs to be supplied to `blur_function`
	:return: Image with faces blurred out

	>>> blurout_faces(image, face_rects, cv2.GaussianBlur, (25, 25), 30)
	>>> blurout_faces(image, face_rects, cv2.medianBlur, 13)
	"""
	for (x, y, w, h) in face_rects:
		center_x, center_y = x + (w // 2), y + (h // 2)

		# Create circular mask around a face
		mask = np.zeros(image.shape[:2], dtype="uint8")
		cv2.circle(mask, (center_x, center_y), min(w, h), 1, -1)

		# Create the inverse of the circular mask
		mask_inverse = np.ones(image.shape[:2], dtype="uint8")
		cv2.circle(mask_inverse, (center_x, center_y), min(w, h), 0, -1)

		# Blur the whole image
		# TODO: some optimization here would be helpful (not to blur the whole image)
		blurred = blur_function(image, *args, **kwargs)
		face_blurred = cv2.bitwise_and(blurred, blurred, mask=mask)

		# Apply the inverse mask to leave some room for the blurred face
		image_with_hole = cv2.bitwise_and(image, image, mask=mask_inverse)
		image = cv2.add(image_with_hole, face_blurred)

	return image
