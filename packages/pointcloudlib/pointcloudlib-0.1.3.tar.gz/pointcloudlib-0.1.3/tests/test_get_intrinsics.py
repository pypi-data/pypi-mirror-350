# import unittest
# import numpy as np
# from ImageBased3DPointCloudLibrary.utils import *


# class TestPointCloud(unittest.TestCase):
#     def test_valid_inputs(self):
#         H, W, fov = 480, 640, 55
#         intrinsics = get_intrinsics(H, W, fov)

#         # Check shape
#         self.assertEqual(intrinsics.shape, (3, 3))

#         # Check the values
#         f = 0.5 * W / np.tan(0.5 * fov * np.pi / 180)
#         expected = np.array([[f, 0, W / 2], [0, f, H / 2], [0, 0, 1]])
#         np.testing.assert_array_almost_equal(intrinsics, expected)

#     def test_get_intrinsics_zero_dimensions(self):
#         with self.assertRaises(ZeroDivisionError):
#             get_intrinsics(0, 640, 55)
#         with self.assertRaises(ZeroDivisionError):
#             get_intrinsics(480, 0, 55)

#     def test_get_intrinsics_negative_dimensions(self):
#         with self.assertRaises(ValueError):
#             get_intrinsics(-480, 640, 55)
#         with self.assertRaises(ValueError):
#             get_intrinsics(480, -640, 55)

#     def test_get_intrinsics_invalid_fov(self):
#         with self.assertRaises(ValueError):
#             get_intrinsics(480, 640, -10)
#         with self.assertRaises(ValueError):
#             get_intrinsics(480, 640, 0)
#         with self.assertRaises(ValueError):
#             get_intrinsics(480, 640, 200)  # Unreasonably large fov

#     def test_get_intrinsics_non_integer_inputs(self):
#         with self.assertRaises(TypeError):
#             get_intrinsics("480", 640, 55)
#         with self.assertRaises(TypeError):
#             get_intrinsics(480, "640", 55)
#         with self.assertRaises(TypeError):
#             get_intrinsics(480, 640, "55")
#         with self.assertRaises(TypeError):
#             get_intrinsics(480.5, 640, 55)
#         with self.assertRaises(TypeError):
#             get_intrinsics(480, 640.5, 55)
#         with self.assertRaises(TypeError):
#             get_intrinsics(480, 640, 55.5)
