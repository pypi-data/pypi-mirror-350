import unittest
import numpy as np
from ImageBased3DPointCloudLibrary.point_cloud_generator import *


class TestPointCloud(unittest.TestCase):
    def test_point_cloud_from_image_valid_input(self):
        image = np.zeros((10, 10, 3))
        depth_estimation = np.ones((10, 10)) * 100

        pcd = point_cloud_from_image(image, depth_estimation)

        self.assertIsInstance(pcd, o3d.geometry.PointCloud),
        self.assertGreater(len(pcd.points), 0)

    def test_point_cloud_from_image_depth_with_zeros(self):
        image = np.zeros((10, 10, 3))
        depth_estimation = np.zeros((10, 10))

        pcd = point_cloud_from_image(image, depth_estimation)

        self.assertIsInstance(pcd, o3d.geometry.PointCloud),
        self.assertEqual(len(pcd.points), 0)

    def test_point_cloud_from_image_image_resizing(self):
        image = np.zeros((20, 20, 3))
        depth_estimation = np.ones((10, 10))

        pcd = point_cloud_from_image(image, depth_estimation)

        self.assertGreater(len(pcd.points), 0)

    def test_point_cloud_from_image_no_camera_intrinsics(self):
        image = np.zeros((10, 10, 3))
        depth_estimation = np.ones((10, 10)) * 100

        pcd = point_cloud_from_image(image, depth_estimation)

        self.assertGreater(len(pcd.points), 0)

    def test_point_cloud_from_image_scale_ratio(self):
        image = np.zeros((10, 10, 3))
        depth_estimation = np.ones((10, 10)) * 100
        scale_ratio = 200

        pcd = point_cloud_from_image(image, depth_estimation, scale_ratio)

        self.assertIsInstance(pcd, o3d.geometry.PointCloud),
        self.assertGreater(len(pcd.points), 0)
