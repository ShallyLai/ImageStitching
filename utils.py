import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from options import args

opt_dir = args.out_dir

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
    pano_file = args.pano_file
    with open(os.path.join(dir_name, pano_file)) as f:
        all = f.readlines()
        for i in range(len(all)):  
            if(i != 0 and all[i - 1] == '\n' and all[i + 1] == '\n'):
                focals.append(float(all[i]))
    return focals

# Plot orientation
def plot_orientation(dx, dy, m, theta):
    fig, ax = plt.subplots(2, 2, figsize=(5, 6))
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
    
    plt.tight_layout()
    fig.savefig(  os.path.join(opt_dir, 'orientation.png') )

# Plot features
def plot_features(im, R, features, corner):
    h, w, c = im.shape
    
    feature_points = np.copy(im)
    for i in range(len(features)):
        cv2.circle(feature_points, (features[i][1], features[i][0]), radius=1, color=[255, 0, 0], thickness=1, lineType=1) 
        
    fig, ax = plt.subplots(1, 3, figsize=(10, 5))
    ax[0].set_title('Original')
    ax[0].imshow(im)
    ax[0].axis('off')

    ax[1].set_title('Feature Points')
    ax[1].imshow(feature_points)
    ax[1].axis('off')

    ax[2].set_title('R')
    ax[2].imshow(np.log(R), cmap='jet')
    ax[2].set_yticklabels([])
    ax[2].set_xticklabels([])

    # ax[1, 1].set_title('Corners')
    # ax[1, 1].imshow(corner, cmap='gist_gray')
    
    plt.savefig( os.path.join(opt_dir, 'features.png') )

# Plot matches
def plot_stitching(img1, img2, matches, stitch_img):
    h1, w1, c1 = img1.shape
    h2, w2, c2 = img2.shape
    s = 50

    ori_img = np.zeros((max(h1, h2), w1+s+w2, 3), dtype=np.uint8) + 255
    ori_img[:h1, :w1] = img1
    ori_img[:h2, w1+s:] = img2

    match_img = np.zeros((max(h1, h2), w1+s+w2, 3), dtype=np.uint8) + 255 
    match_img[:h1, :w1] = img1
    match_img[:h2, w1+s:] = img2

    fig, ax = plt.subplots(3, 1, figsize=(5, 8))
    ax[0].set_title('Original Images')
    ax[0].imshow(ori_img)
    ax[0].axis('off')

    ax[1].set_title('Inlier Matches')
    ax[1].imshow(match_img)
    ax[1].axis('off')
    for f1, f2 in matches:
        x = [f1[1], w1+s+f2[1]]
        y = [f1[0], f2[0]]
        ax[1].plot(x, y, linewidth=1, marker='o', markersize=2)

    ax[2].set_title('Stitching')
    ax[2].imshow(stitch_img.astype('uint8'))
    ax[2].axis('off')
    
    plt.tight_layout()
    plt.savefig( os.path.join(opt_dir, 'stitching.png') )