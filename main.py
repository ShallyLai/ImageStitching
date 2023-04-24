import cv2
import numpy as np
from tqdm import tqdm
from options import args
import os

from utils import read_files, get_focals, plot_orientation, plot_features, plot_stitching
from detection import harris_corner_detector
from cylindrical import cylinder_warp
from description import assign_orientation, feature_description, simple_descriptor
from matching import feature_matching, ransac
from stitching import image_stitching


dir_name = args.src_dir

# tmp_dir = "./tmp"
# if(not os.path.exists(tmp_dir)): 
# 	os.mkdir(tmp_dir)

opt_dir = args.out_dir
if(not os.path.exists(opt_dir)): 
    os.mkdir(opt_dir)

# Create a list of input images
images = read_files(dir_name)

# Get focal information
focals = get_focals(dir_name)

print('Cylinder Warp')
warp_images = []
for i in tqdm(range(len(images))):
    warp_images.append(cylinder_warp(images[i], focals[i]))
    # cv2.imwrite(tmp_dir + '/warp' + str(i) + '.png', warp_images[i])

print('\nFeature Detection & Feature Description')
image_corners = []
R = []
image_features = []
descriptions = []
for i in tqdm(range(len(warp_images))):
    corner, r, dx, dy, dx2, dy2, features = harris_corner_detector(warp_images[i], ksize=3, k=0.04, threshold=args.t)
    
    # Use descriptor in SIFT
    if args.sift == True: 
        m, theta, theta_bin = assign_orientation(dx, dy, dx2, dy2)

        # Plot features and orientation
        if i == 0 and args.plot == True:
            plot_features(warp_images[i], r, features, corner)
            plot_orientation(dx, dy, m, theta)
    
        feature_vectors = feature_description(features, m, theta_bin)
    # Use simplest descriptor
    else:
        feature_vectors = simple_descriptor(warp_images[i], features)
    
    descriptions.append(feature_vectors)
    image_features.append(features)
    image_corners.append(corner)
    R.append(r)
    # cv2.imwrite(tmp_dir + '/harris'+str(i)+'.png', image_corners[i])

print("\nFeature Matching & Image Stitching")
drift  = 0
for i in tqdm((range(len(warp_images) - 1))):
    img1_des = descriptions[i]
    img2_des = descriptions[i+1]
    img1_fea = image_features[i]
    img2_fea = image_features[i+1]
    matches = feature_matching(img1_des, img2_des, img1_fea, img2_fea)
    shift, inlier_matches = ransac(matches)

    if i == 0:
        result, h = image_stitching(warp_images[i], warp_images[i+1], shift, 0, i)
        # Plot stitching
        if args.plot == True:
            plot_stitching(warp_images[i], warp_images[i+1], inlier_matches, result)
    else:
        result, h = image_stitching(result, warp_images[i+1], shift, h, i)

    drift += shift[0] * np.sign(shift[1])

cv2.imwrite(os.path.join(opt_dir, 'result_panorama.png'), result)

# Calculate the new height of the image
new_height = result.shape[0] - abs(drift)

p1 = np.float32([[0, 0], [result.shape[1], drift], [result.shape[1], result.shape[0]]])
p2 = np.float32([[0, 0], [result.shape[1], 0], [result.shape[1], result.shape[0] - drift]])

# Define the transformation matrix
M = cv2.getAffineTransform(p1, p2)

# Apply the transformation to the image
if drift > 0:
    new_img = cv2.warpAffine(result, M, (result.shape[1], new_height))
else:
    new_img = cv2.warpAffine(result, M, (result.shape[1], new_height), dst=np.zeros_like(result))

new_img = new_img[10:new_img.shape[0]-10, 5:new_img.shape[1]-5]   
cv2.imwrite(os.path.join(opt_dir, 'result.png'), new_img)
