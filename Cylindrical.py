import numpy as np
import cv2

def cylinder_warp(image, f):
    # Get image size
    h, w = image.shape[:2]
    
    # Create output image
    out = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Define cylinder parameters
    cx, cy = w / 2, h / 2
    r = f
    
    # Iterate over every pixel in the output image
    for x in range(w):
        for y in range(h):
            if r == 0:
                r += 1e-8
            # Calculate the corresponding point in the input image
            theta = (x - cx) / r
            h_coord = (y - cy) / r 
            X = np.sin(theta)
            Y = h_coord
            Z = np.cos(theta)
            x_in = f * X / Z + cx
            y_in = f * Y / Z + cy
            
            # Interpolate the pixel value at the corresponding point
            if x_in >= 0 and x_in < w and y_in >= 0 and y_in < h:
                out[y, x] = cv2.getRectSubPix(image, (1, 1), (x_in, y_in))
    
    out = out[:, 8:w-8]
    
    return out
