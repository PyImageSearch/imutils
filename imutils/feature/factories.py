#from .descriptors.rootsift import RootSIFT
from ..convenience import is_cv2
import cv2

if is_cv2():
    FeatureDetector_create = cv2.FeatureDetector_create
    DescriptorExtractor_create = cv2.DescriptorExtractor_create
else:
    try:
        _DETECTOR_FACTORY = {"SIFT": cv2.xfeatures2d.SIFT_create,
                             "SURF": cv2.xfeatures2d.SURF_create,
                             "STAR": cv2.xfeatures2d.StarDetector_create,
                             "MSER": cv2.MSER_create,
                             "FAST": cv2.FastFeatureDetector_create,
                             "BRISK": cv2.BRISK_create,
                             "ORB": cv2.ORB_create
                             }

        _EXTRACTOR_FACTORY = {"SIFT": cv2.xfeatures2d.SIFT_create,
                              #"ROOTSIFT": RootSIFT,
                              "SURF": cv2.xfeatures2d.SURF_create,
                              "BRIEF": cv2.xfeatures2d.BriefDescriptorExtractor_create,
                              "ORB": cv2.ORB_create,
                              "BRISK": cv2.BRISK_create,
                              "FREAK": cv2.xfeatures2d.FREAK_create
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
