import cv2
import numpy as np

# Harris Corner Detector
def harris_corner_detector(image, ksize=3, k=0.04, threshold=0.01):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Compute image gradients
    dx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize)
    dy = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize)

    # Compute the products of gradients at each pixel
    dx2 = dx ** 2
    dy2 = dy ** 2
    dxy = dx * dy

    # Compute sums of products of gradients for each pixel
    S_dx2 = cv2.GaussianBlur(dx2, (5, 5), 0)
    S_dy2 = cv2.GaussianBlur(dy2, (5, 5), 0)
    S_dxy = cv2.GaussianBlur(dxy, (5, 5), 0)

    # Compute Harris Corner Detector response R
    det_M = (S_dx2 * S_dy2) - (S_dxy ** 2)
    trace_M = S_dx2 + S_dy2
    R = det_M - (k * (trace_M ** 2))

    # Find the locations of the detected corners
    height, width, _ = image.shape
    corner = np.zeros_like(R, dtype = np.uint8)
    rMax = R.max() * threshold

    # Reduce the corner to find corner locations, window = 5
    for i in range(10, height - 10):
        for j in range(10, width - 10):
            if R[i, j] > rMax and R[i, j] == np.max(R[(i - 2):(i + 3), (j - 2):(j + 3)]):
                corner[i, j] = 255

    return corner, R

