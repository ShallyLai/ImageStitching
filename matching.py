import numpy as np
from scipy.spatial import distance

def ransac(matches, n=1, k=2000, t=3):
    k = len(matches)

    inlier_max = 0
    best_shift = []
    
    matches = np.array(matches)
    for i in range(k):
        shift =  matches[i][1] - matches[i][0]
        d = np.abs( matches[:, 0] - matches[:, 1] + shift )
        d = np.sqrt(np.sum(d**2, 1))
        inliers = np.sum( d < t )
        inlier_index = np.where( d < t )
        if inliers > inlier_max:
            inlier_max = inliers
            inlier_matches = matches[inlier_index]
            best_shift = shift

    #best_shift = np.array(best_shift).astype(int)
    #print(best_shift)
    return best_shift, inlier_matches
       

def feature_matching(d1, d2, f1, f2):
    matches = []
    distances = distance.cdist(d1, d2)
    '''
    distances = 
        d21 d22 d23
     d11
     d12
     d13
    '''
    sorted_row_i = np.argsort((distances))
    for i, row in enumerate(sorted_row_i):
        closest_d = distances[i, row[0]]
        second_closest_d = distances[i, row[1]]
        if closest_d / (second_closest_d+1e-8) < 0.8:
            match  = [f1[i], f2[row[0]]]
            matches.append(match)
    
    return matches 

