import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


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

# Plot Orientation
def plot_orientation(dx, dy, m, theta):
    fig, ax = plt.subplots(2,2,figsize=(10,10))
    ax[0,0].set_title('dx')
    ax[0,0].imshow(dx)
    ax[0,0].axis('off')

    ax[0,1].set_title('dy')
    ax[0,1].imshow(dy)
    ax[0,1].axis('off')
    
    ax[1,0].set_title('magnitude')
    ax[1,0].imshow(m)
    ax[1,0].axis('off')

    ax[1,1].set_title('theta')
    ax[1,1].imshow(theta, cmap='hsv')
    ax[1,1].axis('off')
    
    fig.savefig('orientation.png')
