import numpy as np
from scipy.spatial import distance

def ransac(matches, k=3000, t=3):
    inlier_max = 0
    best_shift = []
    matches = np.array(matches)
    for i in range(k):
        sample_i = np.random.randint(0, len(matches)-1)
        shift = matches[sample_i][1] - matches[sample_i][0] #right-left
        d = matches[:, 1] - ( matches[:, 0] + shift )  
        inliers = np.sum( np.sqrt(np.sum(d**2, 1)) < t )
        if inliers > inlier_max:
            inlier_max = inliers
            best_shift = shift
    return best_shift
       

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
    
    return ransac(matches) 

