import os
import runpy
import sys
import unittest
from unittest.mock import Mock, patch


class RangeDetectorTest(unittest.TestCase):
    def test_trackbar_ranges(self):
        cv2 = Mock()
        script = os.path.join(os.path.dirname(__file__), '..', 'bin',
                              'range-detector')
        with patch.dict(sys.modules, {'cv2': cv2}):
            setup = runpy.run_path(script)['setup_trackbars']
        for color_space in ('HSV', 'RGB'):
            with self.subTest(color_space=color_space):
                cv2.reset_mock()
                setup(color_space)
                calls = [call.args[:4]
                         for call in cv2.createTrackbar.call_args_list]
                expected = []
                for bound in ('MIN', 'MAX'):
                    for channel in color_space:
                        limit = 179 if channel == 'H' else 255
                        initial = 0 if bound == 'MIN' else limit
                        expected.append((channel + '_' + bound, 'Trackbars',
                                         initial, limit))
                self.assertEqual(calls, expected)
