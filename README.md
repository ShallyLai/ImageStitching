# Image Stitching


#### Feature Description
We implemented the feature description method in SIFT algorithm.
It can be divided into two main steps, the first one is orientation assignment, and the second one is keypoint description.

The orientation assignment refers to assigning a dominant orientation to each keypoint. In this step, the SIFT algorithm computes gradient magnitude and orientation histograms in the image region surrounding the keypoint, and selects the orientation with the highest histogram peak as the keypoint's dominant orientation.

The feature description refers to converting the image region surrounding each keypoint into a vector that describes the keypoint's features. In this step, the SIFT algorithm divides the image region surrounding the keypoint into a number of subregions, computes the gradient magnitude and orientation for each subregion, and combines this information into a vector. These vectors are then combined into a SIFT feature vector that represents the keypoint. This feature vector is invariant to scale and rotation, and can be used for image matching.