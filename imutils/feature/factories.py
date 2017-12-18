from ..convenience import is_cv2
import cv2
from .dense import DENSE
from .gftt import GFTT
from .harris import HARRIS
from .rootsift import RootSIFT

if is_cv2():
    def FeatureDetector_create(method):
        method = method.upper()
        if method == "DENSE":
            return DENSE()
        elif method == "GFTT":
            return GFTT()
        elif method == "HARRIS":
            return HARRIS()
        return cv2.FeatureDetector_create(method)

    def DescriptorExtractor_create(method):
        method = method.upper()
        if method == "ROOTSIFT":
            return RootSIFT()
        return cv2.DescriptorExtractor_create(method)

    def DescriptorMatcher_create(method):
        return cv2.DescriptorMatcher_create(method)

else:
    try:
        _DETECTOR_FACTORY = {"BRISK": cv2.BRISK_create,
                             "DENSE": DENSE,
                             "FAST": cv2.FastFeatureDetector_create,
                             "GFTT": GFTT,
                             "HARRIS": HARRIS,
                             "MSER": cv2.MSER_create,
                             "ORB": cv2.ORB_create,
                             "SIFT": cv2.xfeatures2d.SIFT_create,
                             "SURF": cv2.xfeatures2d.SURF_create,
                             "STAR": cv2.xfeatures2d.StarDetector_create
                             }

        _EXTRACTOR_FACTORY = {"SIFT": cv2.xfeatures2d.SIFT_create,
                              "ROOTSIFT": RootSIFT,
                              "SURF": cv2.xfeatures2d.SURF_create,
                              "BRIEF": cv2.xfeatures2d.BriefDescriptorExtractor_create,
                              "ORB": cv2.ORB_create,
                              "BRISK": cv2.BRISK_create,
                              "FREAK": cv2.xfeatures2d.FREAK_create
                              }

        _MATCHER_FACTORY = {"BruteForce": cv2.DESCRIPTOR_MATCHER_BRUTEFORCE,
                           "BruteForce-SL2": cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_SL2,
                           "BruteForce-L1": cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_L1,
                           "BruteForce-Hamming": cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING,
                           "FlannBased": cv2.DESCRIPTOR_MATCHER_FLANNBASED
                           }

    except AttributeError:
        _DETECTOR_FACTORY = {"MSER": cv2.MSER_create,
                             "FAST": cv2.FastFeatureDetector_create,
                             "BRISK": cv2.BRISK_create,
                             "ORB": cv2.ORB_create
                             }

        _EXTRACTOR_FACTORY = {"ORB": cv2.ORB_create,
                              "BRISK": cv2.BRISK_create
                              }

    _CONTRIB_FUNCS = {"SIFT", "ROOTSIFT", "SURF", "STAR", "BRIEF", "FREAK"}


    def FeatureDetector_create(detector, *args, **kw_args):
        """

        :param detector: string of the type of keypoint detector to return
        :param args: positional arguments for detector
        :param kw_args: keyword arguments for detector
        :return: the key point detector object
        """
        try:
            detr = _DETECTOR_FACTORY[detector.upper()]
        except KeyError:
            if detector.upper() in _CONTRIB_FUNCS:
                msg = "OpenCV needs to be compiled with opencv_contrib to support {}".format(detector)
                raise AttributeError(msg)
            raise AttributeError("{} not a supported detector".format(detector))

        return detr(*args, **kw_args)


    def DescriptorExtractor_create(extractor, *args, **kw_args):
        """

        :param extractor: string of the type of descriptor extractor to return
        :param args: positional arguments for extractor
        :param kw_args: keyword arguments for extractor
        :return: the key extractor object
        """
        try:
            extr = _EXTRACTOR_FACTORY[extractor.upper()]
        except KeyError:
            if extractor.upper() in _CONTRIB_FUNCS:
                msg = "OpenCV needs to be compiled with opencv_contrib to support {}".format(extractor)
                raise AttributeError(msg)
            raise AttributeError("{} not a supported extractor".format(extractor))

        return extr(*args, **kw_args)

    def DescriptorMatcher_create(matcher):
        """

        :param matcher: string of the type of descriptor matcher to return
        :return: the matcher int
        """
        try:
            extr = _MATCHER_FACTORY[matcher]
        except KeyError:
            raise AttributeError("{} not a supported matcher".format(matcher))

        return cv2.DescriptorMatcher_create(extr)
