import open3d as o3d
import numpy as np


class AlignmentResult:
    """
    This class is used to store the results of the alignment process.
    """

    def __init__(self):
        self.voxel_size = None
        self.radius_normal = None
        self.radius_feature = None
        self.distance_threshold = None
        self.fitness = None
        self.inlier_rmse = None
        self.correspondence_set_size = None
        self.source_initial_length = None
        self.source_downsampled_length = None
        self.target_initial_length = None
        self.target_downsampled_length = None
        self.transformation = None

    def print_result(self):
        """
        Prints the results of the alignment process.
        """
        print(f"Voxel size: {self.voxel_size}")
        print(f"Radius normal: {self.radius_normal}")
        print(f"Radius feature: {self.radius_feature}")
        print(f"Distance threshold: {self.distance_threshold}")
        print(f"Fitness: {self.fitness}")
        print(f"Inlier RMSE: {self.inlier_rmse}")
        print(f"Correspondence set size: {self.correspondence_set_size}")
        print(f"Correspondence percentage: {self.correspondace_percentage():.2f}%")
        print(f"Source initial length: {self.source_initial_length}")
        print(f"Source downsampled length: {self.source_downsampled_length}")
        print(f"Target initial length: {self.target_initial_length}")
        print(f"Target downsampled length: {self.target_downsampled_length}")
        print(f"Transform: {self.transformation}")

    def correspondace_percentage(self):
        """
        Returns the percentage of correspondences found in the alignment process.

        Returns:
            float: The percentage of correspondences found.
        """
        porc = (
            1
            / 2
            * 100
            * (
                self.correspondence_set_size / self.source_downsampled_length
                + self.correspondence_set_size / self.target_downsampled_length
            )
        )
        return porc

    def is_good_alignment(self, fitness_threshold=0.5, rmse_threshold=1.0):
        """
        Returns True if alignment is considered successful based on thresholds.

        Args:
            fitness_threshold (float): The fitness threshold. Default is 0.5.
            rmse_threshold (float): The RMSE threshold. Default is 1.0.

        Returns:
            bool: True if alignment is considered successful based on thresholds.
        """
        return self.fitness > fitness_threshold and self.inlier_rmse < rmse_threshold


def align_point_clouds(
    source: o3d.geometry.PointCloud,
    target: o3d.geometry.PointCloud,
    downsample_to_n_points: int = 150000,
    radius_normal: float = None,
    max_nn_normals: int = 30,
    radius_feature: float = None,
    max_nn_fpfh: int = 100,
    distance_threshold: float = None,
    ransac_n: int = 3,
    max_iter: int = 100000,
    confidence: float = 0.999,
):
    """
    This function aligns two point clouds using the Fast Point Feature Histograms (FPFH) algorithm.
    Before aligning the point clouds, a voxel size is calculated to downsample the point clouds to work with downsample_to_n_points.
    After that, normals are computed for the downsampled point clouds and the FPFH features are calculated.
    Checkers used are:
    - CorrespondenceCheckerBasedOnEdgeLength(0.9)
    - CorrespondenceCheckerBasedOnDistance(distance_threshold)

    Args:
        - source (o3d.geometry.PointCloud): The source point cloud.
        - target (o3d.geometry.PointCloud): The target point cloud.
        - downsample_to_n_points (int): The number of points to work with for downsampling. Defatul is 150000
        - radius_normal (float): Search radius for normal compute. Default is two times the voxel size
        - max_nn_normals (int): At maximum max_nn_normals will be search for the normal compute Default is 30
        - radius_feature (float): Search radius for FPFH features. Default is five times the voxel size
        - max_nn_fpfh (int): At maximum max_nn_fpfh will be search for the featrue compute. Default is 100
        - distance_threshold (float): Maximum correspondence points-pair distance for the feature matching.Default is 1.5 times the voxel size
        - ransac_n (int): Fit RANSAC with ransac_n correspondences. Default is 3
        - max_iter (int): Maximum iteration before iteration stops. Default is 100000
        - confidence (float): Desired probability of success. Used for estimating early termination. Use 1.0 to avoid early termination for RANSAC criteria.Default is  0.999

    Returns:
        - dict: A dictionary containing information of the alignment process.
        - np.ndarray: The transformation matrix that aligns the source point cloud to the target point cloud.

    """
    _check_inputs(source, target, downsample_to_n_points)

    voxel_size = _calc_voxel_size(source, target, downsample_to_n_points)

    radius_normal = voxel_size * 2 if not radius_normal else radius_normal
    radius_feature = voxel_size * 5 if not radius_feature else radius_feature
    results = AlignmentResult()

    source_down, source_fpfh = _preprocess_point_cloud(
        source,
        voxel_size=voxel_size,
        radius_normal=radius_normal,
        max_nn_normals=max_nn_normals,
        radius_feature=radius_feature,
        max_nn_fpfh=max_nn_fpfh,
        results=results,
        key="source",
    )
    target_down, target_fpfh = _preprocess_point_cloud(
        target,
        voxel_size=voxel_size,
        radius_feature=radius_feature,
        radius_normal=radius_normal,
        results=results,
        max_nn_normals=max_nn_normals,
        max_nn_fpfh=max_nn_fpfh,
        key="target",
    )

    distance_threshold = (
        voxel_size * 1.5 if not distance_threshold else distance_threshold
    )

    result = _execute_global_registration(
        source_down=source_down,
        target_down=target_down,
        source_fpfh=source_fpfh,
        target_fpfh=target_fpfh,
        distance_threshold=distance_threshold,
        ransac_n=ransac_n,
        confidence=confidence,
        max_iter=max_iter,
    )

    results.voxel_size = voxel_size
    results.radius_normal = radius_normal
    results.radius_feature = radius_feature
    results.distance_threshold = distance_threshold
    results.fitness = result.fitness
    results.inlier_rmse = result.inlier_rmse
    results.correspondence_set_size = len(np.asarray(result.correspondence_set))
    results.transformation = result.transformation

    return results


def _calc_voxel_size(source, target, downsample_to_n_points):
    initial_voxel_size = 0.1
    voxel_size_source = _compute_voxel_size(
        source, initial_voxel_size, downsample_to_n_points
    )
    voxel_size_target = _compute_voxel_size(
        target, initial_voxel_size, downsample_to_n_points
    )
    return np.mean([voxel_size_source, voxel_size_target])


def _compute_voxel_size(point_cloud, initial_voxel_size, target_points):
    voxel_size = initial_voxel_size
    downsampled = point_cloud
    while len(downsampled.points) > target_points:
        voxel_size += 0.01
        downsampled = point_cloud.voxel_down_sample(voxel_size=voxel_size)
    return voxel_size


def _preprocess_point_cloud(
    pcd,
    voxel_size,
    radius_normal,
    max_nn_normals,
    radius_feature,
    max_nn_fpfh,
    results,
    key,
):
    pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)

    radius_normal = voxel_size * 2
    # Noramls are used to calculate the FPFH features
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(
            radius=radius_normal, max_nn=max_nn_normals
        )
    )

    radius_feature = voxel_size * 5
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=max_nn_fpfh),
    )

    if key == "source":
        results.source_initial_length = len(pcd.points)
        results.source_downsampled_length = len(pcd_down.points)
    elif key == "target":
        results.target_initial_length = len(pcd.points)
        results.target_downsampled_length = len(pcd_down.points)

    return pcd_down, pcd_fpfh


def _execute_global_registration(
    source_down,
    target_down,
    source_fpfh,
    target_fpfh,
    distance_threshold,
    ransac_n,
    confidence,
    max_iter,
):

    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down,
        target_down,
        source_fpfh,
        target_fpfh,
        True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        ransac_n=ransac_n,
        checkers=[  # Pruning, points that pass the pruning will be subject to RANSAC
            # Checking if the edeges of source and target are about 0.9 of each other
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            # Checking if the distance between the points is less than the threshold
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold
            ),
        ],
        criteria=o3d.pipelines.registration.RANSACConvergenceCriteria(
            max_iter, confidence
        ),
    )  # max_iter, confidence
    return result


def _check_inputs(source, target, work_with_n):
    if not isinstance(source, o3d.geometry.PointCloud):
        raise TypeError("source must be of type open3d.geometry.PointCloud")
    if not isinstance(target, o3d.geometry.PointCloud):
        raise TypeError("target must be of type open3d.geometry.PointCloud")
    if not isinstance(work_with_n, int):
        raise TypeError("work_with_n must be of type int")
    if work_with_n <= 10000:
        raise TypeError("work_with_n should be greater than 10000")
