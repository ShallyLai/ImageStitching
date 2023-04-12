import os
import cv2
import numpy as np

# Load input images
def read_files(dir_name):
    images = []
    for filename in np.sort(os.listdir(dir_name)):
        if os.path.splitext(filename)[1] in ['.png', '.jpg', '.JPG', '.PNG']: # Only read png or jpg files
            img = cv2.imread(os.path.join(dir_name, filename))
            images.append(img)
    return images

# A measure of the distance between the camera lens and the image sensor
def get_focals(dir_name):
    focals = []
    with open(os.path.join(dir_name, 'pano.txt')) as f:
        all = f.readlines()
        for i in range(len(all)):  
            if(i != 0 and all[i - 1] == '\n' and all[i + 1] == '\n'):
                focals.append(float(all[i]))
    return focals
