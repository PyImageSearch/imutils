# author:    Adrian Rosebrock
# website:   http://www.pyimagesearch.com

# import the necessary packages
from scipy.spatial import distance as dist
import numpy as np
import cv2

def order_points(pts):
    # sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]

    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    # now that we have the top-left coordinate, use it as an
    # anchor to calculate the Euclidean distance between the
    # top-left and right-most points; by the Pythagorean
    # theorem, the point with the largest distance will be
    # our bottom-right point
    D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
    (br, tr) = rightMost[np.argsort(D)[::-1], :]

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="float32")

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped

def inverse_four_point_transform(image, warped, pts):
    """Project an edited top-down image back onto four points in an image.

    Return a copy of ``image`` with the quadrilateral replaced by ``warped``.
    The images must have matching dtypes and channel layouts. The source may
    have been resized after four_point_transform, but must be at least 2x2.
    All source pixels, including black and alpha values, are copied without
    alpha blending. Pixels outside the projected source remain unchanged.
    """
    if image.dtype != warped.dtype or image.shape[2:] != warped.shape[2:]:
        raise ValueError("image and warped must have matching dtype and channels")
    height, width = warped.shape[:2]
    if height < 2 or width < 2:
        raise ValueError("warped must be at least 2x2 pixels")

    rect = order_points(np.asarray(pts, dtype="float32"))
    source = np.array([[0, 0], [width - 1, 0],
                       [width - 1, height - 1], [0, height - 1]],
                      dtype="float32")
    matrix = cv2.getPerspectiveTransform(source, rect)
    size = (image.shape[1], image.shape[0])
    projected = cv2.warpPerspective(warped, matrix, size,
                                    borderMode=cv2.BORDER_REPLICATE)
    # Rasterize the destination itself: warping a source mask would expand
    # its half-pixel border when the edited crop has been resized.
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.fillConvexPoly(mask, np.round(rect * 256).astype("int32"), 1, shift=8)
    # OpenCV squeezes a single-channel axis; restore the input's layout.
    if warped.ndim == 3 and projected.ndim == 2:
        projected = projected[:, :, np.newaxis]
    result = image.copy()
    result[mask != 0] = projected[mask != 0]
    return result
