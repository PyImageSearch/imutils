# author:	Adrian Rosebrock
# website:	http://www.pyimagesearch.com

# import the necessary packages

import sys

if sys.version_info[0] < 3:
    from convenience import translate
    from convenience import rotate
    from convenience import resize
    from convenience import skeletonize
    from convenience import opencv2matplotlib
    from convenience import url_to_image
    from convenience import auto_canny
    from convenience import is_cv2
    from convenience import is_cv3
    from convenience import check_opencv_version
else:
    from imutils.convenience import translate
    from imutils.convenience import rotate
    from imutils.convenience import resize
    from imutils.convenience import skeletonize
    from imutils.convenience import opencv2matplotlib
    from imutils.convenience import url_to_image
    from imutils.convenience import auto_canny
    from imutils.convenience import is_cv2
    from imutils.convenience import is_cv3
    from imutils.convenience import check_opencv_version
