import unittest

import numpy as np

from imutils import perspective


class InversePerspectiveTests(unittest.TestCase):
    def test_rectangle_and_black_pixels(self):
        canvas = np.full((12, 14, 3), 100, dtype='uint8')
        points = np.array([[3, 2], [9, 2], [9, 8], [3, 8]], dtype='float32')
        warped = perspective.four_point_transform(canvas, points)
        warped[:] = [0, 50, 200]
        result = perspective.inverse_four_point_transform(canvas, warped, points)
        expected = canvas.copy()
        expected[2:9, 3:10] = [0, 50, 200]
        np.testing.assert_array_equal(result, expected)
        np.testing.assert_array_equal(canvas, np.full_like(canvas, 100))
        np.testing.assert_array_equal(warped[0, 0], [0, 50, 200])
        self.assertFalse(np.shares_memory(result, canvas))

    def test_grayscale_resized_source_and_unordered_points(self):
        canvas = np.full((10, 10), 100, dtype='uint8')
        warped = np.zeros((3, 4), dtype='uint8')
        points = np.array([[7, 7], [2, 2], [2, 7], [7, 2]], dtype='float32')
        expected = canvas.copy()
        expected[2:8, 2:8] = 0
        np.testing.assert_array_equal(
            perspective.inverse_four_point_transform(canvas, warped, points),
            expected)

    def test_perspective_corner_correspondence(self):
        canvas = np.full((20, 20, 3), 99, dtype='uint8')
        warped = np.zeros((8, 9, 3), dtype='uint8')
        colors = [[10, 20, 30], [40, 50, 60], [70, 80, 90], [100, 110, 120]]
        warped[0, 0], warped[0, -1], warped[-1, -1], warped[-1, 0] = colors
        points = np.array([[4, 2], [15, 5], [13, 16], [2, 13]], dtype='float32')
        result = perspective.inverse_four_point_transform(canvas, warped, points)
        for point, color in zip(points.astype(int), colors):
            np.testing.assert_array_equal(result[point[1], point[0]], color)
        np.testing.assert_array_equal(result[0], canvas[0])
        np.testing.assert_array_equal(result[-1], canvas[-1])
        np.testing.assert_array_equal(result[:, 0], canvas[:, 0])

    def test_float_and_four_channels(self):
        canvas = np.ones((8, 8, 4), dtype='float32')
        warped = np.full((3, 3, 4), 0.25, dtype='float32')
        points = np.array([[2, 2], [5, 2], [5, 5], [2, 5]], dtype='float32')
        result = perspective.inverse_four_point_transform(canvas, warped, points)
        self.assertEqual(result.dtype, canvas.dtype)
        np.testing.assert_array_equal(result[3, 3], warped[1, 1])
        np.testing.assert_array_equal(result[0, 0], canvas[0, 0])

    def test_rejects_incompatible_images(self):
        canvas = np.zeros((8, 8, 3), dtype='uint8')
        points = np.array([[2, 2], [5, 2], [5, 5], [2, 5]], dtype='float32')
        for warped in [np.zeros((3, 3), dtype='uint8'),
                       np.zeros((3, 3, 3), dtype='float32'),
                       np.zeros((1, 3, 3), dtype='uint8')]:
            with self.assertRaises(ValueError):
                perspective.inverse_four_point_transform(canvas, warped, points)


if __name__ == '__main__':
    unittest.main()
