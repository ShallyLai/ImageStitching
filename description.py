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
    for i in range(h, h + 4):
        for j in range(w, w + 4):
            index = int(theta[i][j])
            index %= 8
            vector[index] += m[i][j]
    
    return vector


def feature_description(features, m, theta_bin):
    feature_vectors = []

    height, width = theta_bin.shape[:2]
    center = (width/2, height/2)
    
    for h, w in features: # for each vector
        feature_vector = []
        # rotate theta_bin 
        rotate_matrix = cv2.getRotationMatrix2D(center, theta_bin[h,w], 1)
        theta_rotated = cv2.warpAffine(theta_bin[h-8:h+8, w-8:w+8], rotate_matrix, (16, 16))
        m_rotated = cv2.warpAffine(m[h-8:h+8, w-8:w+8], rotate_matrix, (16, 16))
        # patch size 16*16 (subpatch 4*4)
        for i in range(0, 16, 4):
            for j in range(0, 16, 4):
                feature_vector += get_subpatch_vector(i, j, theta_rotated, m_rotated)

        feature_vectors.append(feature_vector)
    
    return feature_vectors

        
