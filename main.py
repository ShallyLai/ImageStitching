import cv2
import numpy as np
from tqdm import tqdm
import argparse
import os

from utils import read_files, get_focals
from FeatureDection import harris_corner_detector
from Cylindrical import cylinder_warp

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
for i in tqdm(range(len(warp_images))):
    h, r = harris_corner_detector(warp_images[i], ksize=3, k=0.04, threshold=0.01)
    hcd.append(h)
    R.append(r)
    cv2.imwrite(tmp_dir + '/harris'+str(i)+'.png', hcd[i])
