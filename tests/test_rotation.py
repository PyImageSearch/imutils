import unittest

import cv2
import numpy as np

import imutils


class RotationTest(unittest.TestCase):
    def test_border_value(self):
        for shape, color in [((20, 20), 255),
                             ((20, 20, 3), (30, 100, 200))]:
            image = np.zeros(shape, dtype=np.uint8)
            for rotate in (imutils.rotate, imutils.rotate_bound):
                with self.subTest(shape=shape, rotate=rotate.__name__):
                    default = rotate(image, 45)
                    explicit = rotate(image, 45, border_value=0)
                    np.testing.assert_array_equal(default, explicit)
                    result = rotate(image, 45, border_value=color)
                    np.testing.assert_array_equal(result[0, 0], color)
                    self.assertEqual(result.shape, default.shape)
                    self.assertEqual(result.dtype, image.dtype)
                    np.testing.assert_array_equal(image, np.zeros_like(image))

    def test_custom_center_and_scale(self):
        image = np.arange(100, dtype=np.uint8).reshape(10, 10)
        matrix = cv2.getRotationMatrix2D((2, 3), 25, 0.5)
        expected = cv2.warpAffine(image, matrix, (10, 10), borderValue=200)
        actual = imutils.rotate(image, 25, (2, 3), 0.5, border_value=200)
        np.testing.assert_array_equal(actual, expected)
