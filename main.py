import cv2
import numpy as np
from tqdm import tqdm
import argparse
import os

from utils import read_files, get_focals, plot_orientation
from FeatureDection import harris_corner_detector
from Cylindrical import cylinder_warp
from feature_desciption import assign_orientation, feature_description

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
#for i in tqdm(range(len(warp_images))):
for i in [0]: #test
    h, r, dx, dy, dx2, dy2, features = harris_corner_detector(warp_images[i], ksize=3, k=0.04, threshold=0.01)
    m, theta, theta_bin = assign_orientation(dx, dy, dx2, dy2)

    plot_orientation(dx, dy, m, theta)#
    
    feature_vectors = feature_description(features, m, theta_bin)

    hcd.append(h)
    R.append(r)
    cv2.imwrite(tmp_dir + '/harris'+str(i)+'.png', hcd[i])
