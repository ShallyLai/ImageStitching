import cv2
import numpy as np

def assign_orientation(ix, iy, ix2, iy2):
    m = (ix2 + iy2) ** (1/2)  # magnitude
    
    theta = np.arctan2(iy,ix) / np.pi * 180
    theta[iy < 0] += 360

    theta_bin = theta // 45  # divide theta into 8 bins (each 45 theta)

    return m, theta, theta_bin
    

def get_subpatch_vector(h, w, theta, m):
    vector = [0 for i in range(8)]
    for i in range(h, h + 5):
        for j in range(w, w + 5):
            index = int(theta[i][j])
            index %= 8
            vector[index] += m[i][j]
    
    return vector


def feature_description(features, m, theta_bin):
    feature_vectors = []

    height, width = theta_bin.shape[:2]
    center = (width/2, height/2)
    
    for h, w in features: # for each feature
        feature_vector = []
        # rotate theta_bin 
        rotate_matrix = cv2.getRotationMatrix2D(center, theta_bin[h,w], 1)
        theta_rotated = cv2.warpAffine(theta_bin[h-10:h+10, w-10:w+10], rotate_matrix, (20, 20))
        m_rotated = cv2.warpAffine(m[h-10:h+10, w-10:w+10], rotate_matrix, (20, 20))
        # patch size 20*20 (subpatch 5*5)
        for i in range(0, 20, 5):
            for j in range(0, 20, 5):
                feature_vector += get_subpatch_vector(i, j, theta_rotated, m_rotated)

        feature_vectors.append(feature_vector)
    
    return feature_vectors


def simple_descriptor(img, features, kernel=4):
    feature_vectors = []
    for h, w in features:
        neightbors = img[h-kernel:h+kernel, w-kernel:w+kernel]
        feature_vectors.append(neightbors.flatten())
    return feature_vectors