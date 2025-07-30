import numpy as np
import copy
import open3d as o3d


def get_intrinsics(H, W, fov=55):
    """
    Calculate the intrinsic matrix of a camera given the height, width and field of view.
    Args:
        - H: Height of the image.
        - W: Width of the image.
        - fov: Field of view of the camera. Default is 55 degrees.
    Returns:
        - np.ndarray: The intrinsic matrix of the camera.
    """
    validate_input(H, W, fov)
    f = 0.5 * W / np.tan(0.5 * fov * np.pi / 180)
    cx = 0.5 * W
    cy = 0.5 * H
    return np.array([[f, 0, cx], [0, f, cy], [0, 0, 1]])


def draw_two_clouds(pcd1, pcd2, transformation=None, diff_color=True):
    """
    This function draws two point clouds in the same window.
    Args:
        - pcd1 (o3d.geometry.PointCloud): The first point cloud.
        - pcd2 (o3d.geometry.PointCloud): The second point cloud.
        - transformation (np.ndarray): The transformation matrix to apply to the pcd1 point cloud. Default is None.
        - diff_color (bool): If True, the pcd1 point cloud will be painted in yellow and the pcd2 point cloud in blue. Default is True.
    """
    pcd1_temp = copy.deepcopy(pcd1)
    pcd2_temp = copy.deepcopy(pcd2)
    if diff_color:
        pcd1_temp.paint_uniform_color([1, 0.706, 0])
        pcd2_temp.paint_uniform_color([0, 0.651, 0.929])
    if transformation is not None:
        pcd1_temp.transform(transformation)
    o3d.visualization.draw_geometries([pcd1_temp, pcd2_temp])


def validate_input(H, W, fov):
    if H == 0 or W == 0:
        raise ZeroDivisionError("Height and width must be greater than zero.")
    if H < 0 or W < 0:
        raise ValueError("Height and width must be positive.")
    if fov <= 0 or fov > 180:
        raise ValueError("Field of view must be in the range [0, 180].")
    if not isinstance(H, int) or not isinstance(W, int) or not isinstance(fov, int):
        raise TypeError("Height, width and field of view must be integers.")
