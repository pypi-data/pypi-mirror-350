# PointCloudLib

This Python library is designed for image processing with a focus on 3D environment modeling. It is part of the final graduation project at the Costa Rica Institute of Technology.

## Requirements:

The project was developed using Python 3.12. It is recommended to use this version to avoid compatibility issues. Below is a list of the required dependencies to run the project. The dependencies are included in the `requirements.txt` file.

- transformers==4.48.0
- pillow==11.1.0
- open3d==0.19.0
- opencv-python==4.11.0.86
- torch==2.6.0
- sphinx==8.1.3 (for documentation)

The library is available for installation on pip [(page)](https://pypi.org/project/pointcloudlib/0.1/). To install the latest version, simply run the following command:


```
pip install pointcloudlib
```


## Generating Documentation

To generate the project documentation, navigate to the docs folder and run the following command:

```
cd docs
make.bat html
```

Once the documentation is generated, you can view it in the `docs/_build/html/index.html file.`

## Library Functions

The library provides the following key functions:
- `depth_estimation_from_image()`: Estimates the depth of an RGB image using a deep learning model.
- `point_cloud_from_image()`:  Generates a point cloud from an RGB image and its corresponding depth image.
- `align_point_clouds()`: Aligns two point clouds using FPFH (Fast Point Feature Histograms).

Additionally, the library includes a function to visualize two aligned point clouds:
- `draw_two_point_clouds()`: Displays two aligned point clouds in the same window.


## Demo

A demo of the library can be found in `demo/generic_pipeline.py`. The following code snippet demonstrates how to load images, estimate depth, generate point clouds, and align them.


```
import cv2
from pointcloudlib import *

image_path1 = "house_left.JPEG"
image_path2 = "house_right.JPEG"

image1 = cv2.imread(image_path1, cv2.IMREAD_COLOR)
image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

image2 = cv2.imread(image_path2, cv2.IMREAD_COLOR)
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
```

Two RGB images from the resources folder are used:

![Image](https://raw.githubusercontent.com/Yorbre25/ImageBased3DPointCloudLibrary/refs/heads/Develop/resources/house_right.JPEG?token=GHSAT0AAAAAAC4WJBKJSVASLZSLTJUIQO3WZ5KI4EA)
![Image](https://raw.githubusercontent.com/Yorbre25/ImageBased3DPointCloudLibrary/refs/heads/Develop/resources/house_left.JPEG?token=GHSAT0AAAAAAC4WJBKJKMDTJCLODVBZ5YF2Z5KI4LA)

```
depth_estimation1 = depth_estimation_from_image(image1)
depth_estimation2 = depth_estimation_from_image(image2)
```

The depth map for each image is calculated. Below is the depth map for image 1, converted to grayscale (this step is not shown in the demo code):

![Image](https://raw.githubusercontent.com/Yorbre25/ImageBased3DPointCloudLibrary/refs/heads/Develop/resources/house_left_depth.png?token=GHSAT0AAAAAAC4WJBKI4BZ3RF6LC2QHTAJYZ5KI5GQ)


Next, point clouds are generated from the images and their corresponding depth maps:
```
source = point_cloud_from_image(image1, depth_estimation1)
target = point_cloud_from_image(image2, depth_estimation2)
```

Statistical outliers are removed from the point clouds to improve the accuracy of the alignment:

```
cl, ind = source.remove_statistical_outlier(nb_neighbors=20, std_ratio=2)
source = source.select_by_index(ind)
cl, ind = target.remove_statistical_outlier(nb_neighbors=20, std_ratio=2)
target = target.select_by_index(ind)
```
Below is the point cloud for image 1 after removing outliers:

![Image](https://raw.githubusercontent.com/Yorbre25/ImageBased3DPointCloudLibrary/refs/heads/Develop/resources/house_left_pcd.gif?token=GHSAT0AAAAAAC4WJBKJK6WLULNNSTAMOUREZ5KI5RA)

The point clouds are aligned, An object called AlignmentResult is returned with the alignment result:
```
result = align_point_clouds(source, target)
result.print_result()
```

The alignment result is shown below:
![Image](https://raw.githubusercontent.com/Yorbre25/ImageBased3DPointCloudLibrary/refs/heads/Develop/resources/alignment_result.png?token=GHSAT0AAAAAAC4WJBKIPRJMV5K43EVSKWAKZ5KI54Q)

The alignment result can be checked to determine if it is a good alignment:

```
print(f"Is it a good aligmnet?: {result.is_good_alignment()}")
```
![Image](https://raw.githubusercontent.com/Yorbre25/ImageBased3DPointCloudLibrary/refs/heads/Develop/resources/is_good_alignment.png?token=GHSAT0AAAAAAC4WJBKIQA54EQSAHLX2ZCEUZ5KI6GA)



The final result of the alignment is shown in the following gif:

![Image](https://raw.githubusercontent.com/Yorbre25/ImageBased3DPointCloudLibrary/refs/heads/Develop/resources/house_alignment.gif?token=GHSAT0AAAAAAC4WJBKJ4DTNXGIN5PDTRLDGZ5KI53Q)


