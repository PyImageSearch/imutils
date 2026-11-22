import importlib
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch


count_module = importlib.import_module("imutils.video.count_frames")


class CountFramesTest(unittest.TestCase):
    def test_modern_opencv_uses_frame_count_property(self):
        for version in ("3.4.0", "4.10.0", "5.0.0"):
            with self.subTest(version=version):
                video = Mock()
                video.get.return_value = 42
                video.read.return_value = (False, None)
                with patch.object(count_module.cv2, "__version__", version), \
                        patch.object(count_module.cv2, "VideoCapture",
                                     return_value=video):
                    self.assertEqual(count_module.count_frames("clip.avi"), 42)
                video.get.assert_called_once_with(
                    count_module.cv2.CAP_PROP_FRAME_COUNT)
                video.read.assert_not_called()
                video.release.assert_called_once_with()

    def test_opencv_two_uses_legacy_property(self):
        video = Mock()
        video.get.return_value = 12
        legacy = SimpleNamespace(CV_CAP_PROP_FRAME_COUNT=123)
        with patch.object(count_module.cv2, "__version__", "2.4.13"), \
                patch.object(count_module.cv2, "cv", legacy, create=True), \
                patch.object(count_module.cv2, "VideoCapture", return_value=video):
            self.assertEqual(count_module.count_frames("clip.avi"), 12)
        video.get.assert_called_once_with(123)
        video.read.assert_not_called()
        video.release.assert_called_once_with()

    def test_manual_override_and_property_failure(self):
        for override in (False, True):
            with self.subTest(override=override):
                video = Mock()
                video.get.side_effect = ValueError("unsupported property")
                video.read.side_effect = [(True, object()), (False, None)]
                with patch.object(count_module.cv2, "__version__", "4.10.0"), \
                        patch.object(count_module.cv2, "VideoCapture",
                                     return_value=video):
                    self.assertEqual(count_module.count_frames(
                        "clip.avi", override=override), 1)
                self.assertEqual(video.get.call_count, 0 if override else 1)
                video.release.assert_called_once_with()
