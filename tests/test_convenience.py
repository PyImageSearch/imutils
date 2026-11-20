import unittest

import cv2
import numpy as np

from imutils import opencv2matplotlib


class TestOpenCVToMatplotlib(unittest.TestCase):
    def test_color_channels_preserve_dtype_and_values(self):
        for dtype in (np.uint8, np.uint16, np.float16, np.float32, np.float64):
            for channels in (3, 4):
                with self.subTest(dtype=dtype, channels=channels):
                    image = np.arange(2 * 3 * channels, dtype=dtype).reshape(
                        2, 3, channels)
                    if np.issubdtype(dtype, np.floating):
                        image /= 25
                    result = opencv2matplotlib(image)
                    self.assertEqual(result.dtype, image.dtype)
                    self.assertEqual(result.shape, (2, 3, 3))
                    np.testing.assert_array_equal(result[..., 0], image[..., 2])
                    np.testing.assert_array_equal(result[..., 1], image[..., 1])
                    np.testing.assert_array_equal(result[..., 2], image[..., 0])
                    self.assertFalse(np.shares_memory(result, image))

    def test_noncontiguous_float_image(self):
        image = np.arange(48, dtype=np.float64).reshape(4, 4, 3)[::2, ::2]
        result = opencv2matplotlib(image)
        np.testing.assert_array_equal(result, image[..., [2, 1, 0]])
        self.assertTrue(result.flags.c_contiguous)

    def test_grayscale_conversion_is_preserved(self):
        gray = np.arange(6, dtype=np.uint8).reshape(2, 3)
        expected = np.repeat(gray[..., None], 3, axis=2)
        np.testing.assert_array_equal(opencv2matplotlib(gray), expected)
        np.testing.assert_array_equal(opencv2matplotlib(gray[..., None]), expected)

    def test_invalid_channel_count_is_rejected(self):
        with self.assertRaises(cv2.error):
            opencv2matplotlib(np.zeros((2, 3, 2), dtype=np.uint8))


if __name__ == '__main__':
    unittest.main()
