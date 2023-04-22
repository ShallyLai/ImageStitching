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
            if img.shape[1] > 600:
                rate = img.shape[1] / 600
                img = cv2.resize(img, (int(img.shape[1] / rate), int(img.shape[0] / rate)))
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

# Plot orientation
def plot_orientation(dx, dy, m, theta):
    fig, ax = plt.subplots(2, 2, figsize=(10, 10))
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

# Plot features
def plot_features(im, R, features, corner):
    h, w, c = im.shape
    
    feature_points = np.copy(im)
    for i in range(len(features)):
        cv2.circle(feature_points, (features[i][1], features[i][0]), radius=1, color=[255, 0, 0], thickness=1, lineType=1) 
        
    fig, ax = plt.subplots(2, 2, figsize=(15, 15))
    ax[0, 0].set_title('Original')
    ax[0, 0].imshow(im)

    ax[0, 1].set_title('Feature Points')
    ax[0, 1].imshow(feature_points); 

    ax[1, 0].set_title('R')
    ax[1, 0].imshow(np.log(R), cmap='jet')

    ax[1, 1].set_title('Corners')
    ax[1, 1].imshow(corner, cmap='gist_gray')
    
    plt.savefig('features.png')

