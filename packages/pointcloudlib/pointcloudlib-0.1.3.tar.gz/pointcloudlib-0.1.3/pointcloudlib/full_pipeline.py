import numpy as np
import cv2
from depth_estimation import depth_estimation_from_image
from point_cloud_generator import point_cloud_from_image
from point_cloud_aligner import align_point_clouds

image_path1 = "house_left.JPEG"
image_path2 = "house_right.JPEG"


def full_pipeline(
    image1: np.ndarray,
    image2: np.ndarray,
):

    depth_estimation1 = depth_estimation_from_image(image1)
    depth_estimation2 = depth_estimation_from_image(image2)

    source = point_cloud_from_image(image1, depth_estimation1)
    target = point_cloud_from_image(image2, depth_estimation2)

    cl, ind = source.remove_statistical_outlier(nb_neighbors=20, std_ratio=2)
    source = source.select_by_index(ind)
    cl, ind = target.remove_statistical_outlier(nb_neighbors=20, std_ratio=2)
    target = target.select_by_index(ind)

    result = align_point_clouds(source, target)
    return result, source, target
