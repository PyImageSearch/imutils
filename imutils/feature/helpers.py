# import the necesasry packages
import cv2

def corners_to_keypoints(corners):
    """function to take the corners from cv2.GoodFeaturesToTrack and return cv2.KeyPoints"""
    return [cv2.KeyPoint(kp[0][0], kp[0][1], 1) for kp in corners]