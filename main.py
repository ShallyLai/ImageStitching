import cv2
import numpy as np
from tqdm import tqdm
import argparse
import os

from utils import read_files, get_focals, plot_orientation
from FeatureDection import harris_corner_detector
from Cylindrical import cylinder_warp
from feature_description import assign_orientation, feature_description
from feature_matching import feature_matching

dir_name = "./parrington"

tmp_dir = "./tmp"
if(not os.path.exists(tmp_dir)): 
	os.mkdir(tmp_dir)

# Create a list of input images
images = read_files(dir_name)

# Get focal information
focals = get_focals(dir_name)

print('Cylinder Warp')
warp_images = []
for i in tqdm(range(len(images))):
    warp_images.append(cylinder_warp(images[i], focals[i]))
    cv2.imwrite(tmp_dir + '/warp'+str(i)+'.png', warp_images[i])


print('Feature Detection')
hcd = []
R = []
image_features = []
descriptions = []
for i in tqdm(range(len(warp_images))):
    h, r, dx, dy, dx2, dy2, features = harris_corner_detector(warp_images[i], ksize=3, k=0.04, threshold=0.01)
    m, theta, theta_bin = assign_orientation(dx, dy, dx2, dy2)

    # Plot orientation
    if i == 0:
        plot_orientation(dx, dy, m, theta)
    
    feature_vectors = feature_description(features, m, theta_bin)
    
    descriptions.append(feature_vectors)
    image_features.append(features)
    hcd.append(h)
    R.append(r)
    cv2.imwrite(tmp_dir + '/harris'+str(i)+'.png', hcd[i])

for i in tqdm((range(len(warp_images)-1))):
    img1_des = descriptions[i]
    img2_des = descriptions[i+1]
    img1_fea = image_features[i]
    img2_fea = image_features[i+1]
    print( feature_matching(img1_des, img2_des, img1_fea, img2_fea) )
