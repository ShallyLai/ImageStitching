# Image Stitching

#### Cylinder Warping
We took an input image and a focal length as arguments and performed cylinder warping on the input image. The output is a new image that has undergone a transformation in which the original image is projected onto a cylindrical surface. 

The code iterates over each pixel in the output image, calculates the corresponding point in the input image, and interpolates the pixel value at that point. The resulting output image has corrected distortion, and the image's visual quality is enhanced.


#### Feature Detection
We achieved the Harris Corner Detector algorithm that the instructor mentioned in class. 

In the function, the image is first converted to grayscale. Then, the image gradients in both the x and y directions are computed. The products of gradients at each pixel are computed using simple arithmetic operations. Next, the sums of products of gradients for each pixel are computed to obtain the Harris Corner Detector response R. Finally, the locations of the detected corners are found by iterating through the image and checking if the response R is greater than the threshold value and is the maximum value in a 5x5 window. The detected corner locations are then returned along with other computed variables.


#### Feature Description
We implemented the feature description method in SIFT algorithm.
It can be divided into two main steps, the first one is orientation assignment, and the second one is keypoint description.

The orientation assignment refers to assigning a dominant orientation to each keypoint. In this step, the SIFT algorithm computes gradient magnitude and orientation histograms in the image region surrounding the keypoint, and selects the orientation with the highest histogram peak as the keypoint's dominant orientation.

The feature description refers to converting the image region surrounding each keypoint into a vector that describes the keypoint's features. In this step, the SIFT algorithm divides the image region surrounding the keypoint into a number of subregions, computes the gradient magnitude and orientation for each subregion, and combines this information into a vector. These vectors are then combined into a SIFT feature vector that represents the keypoint. This feature vector is invariant to scale and rotation, and can be used for image matching.