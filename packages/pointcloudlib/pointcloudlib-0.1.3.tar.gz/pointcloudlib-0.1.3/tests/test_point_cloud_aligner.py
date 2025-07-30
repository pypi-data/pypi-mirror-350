# import unittest
# import numpy as np
# from ImageBased3DPointCloudLibrary.point_cloud_aligner import *


# class TestPointCloud(unittest.TestCase):
#     def test_align_point_clouds_no_o3d_point_cloud_input(self):

#         with self.assertRaises(TypeError):
#             align_point_clouds(1, 2)

#     def test_align_point_clouds_0_n_points(self):
#         source = o3d.geometry.PointCloud()
#         target = o3d.geometry.PointCloud()
#         source.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
#         target.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
#         n_points = 0
#         with self.assertRaises(TypeError):
#             align_point_clouds(source, target, n_points)

#     def test_align_point_clouds_high_n_points(self):
#         source = o3d.geometry.PointCloud()
#         target = o3d.geometry.PointCloud()
#         source.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
#         target.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
#         n_points = 10000000

#         results = align_point_clouds(source, target, n_points)

#         self.assertIsInstance(results, AlignmentResult)

#     def test_align_point_clouds(self):
#         source = o3d.geometry.PointCloud()
#         target = o3d.geometry.PointCloud()
#         source.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
#         target.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))
#         results = align_point_clouds(source, target)
#         self.assertIsInstance(results, AlignmentResult)
