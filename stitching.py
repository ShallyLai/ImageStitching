import numpy as np
import cv2
import os

def image_stitching(right_img, left_img, shift, shift_last_h, i):
    #move left img to align right img
    right_h = right_img.shape[0]
    right_w = right_img.shape[1]
    left_h = left_img.shape[0]
    left_w = left_img.shape[1]

    dh = shift[0]
    dw = shift[1]

    width = right_w + abs(dw)

    if shift_last_h + dh < 0:
        height = right_h + abs(dh + shift_last_h)
    elif dh > 0:
        height = right_h + dh
    else:
        height = right_h

    result_left = np.zeros((height, width, right_img.shape[2]))
    result_right = np.zeros((height, width, right_img.shape[2]))
    result = np.zeros((height, width, right_img.shape[2]))

    # move left & down
    if dw < 0 and (dh + shift_last_h > 0): 
        result_left[-right_h:, :right_w, :] = right_img
        result_right[:left_h, -left_w:, :] = left_img
    
    # move left & up
    elif dw < 0 and (dh + shift_last_h <= 0): 
        result_left[:right_h, :right_w, :] = right_img
        result_right[-left_h:, -left_w:, :] = left_img
    
    # move right & down
    elif dw >= 0 and (dh + shift_last_h > 0): 
        result_left[:left_h, :left_w, :] = left_img
        result_right[-right_h:, -right_w:, :] = right_img
    
    # move right & up
    else:
        result_left[-left_h:, :left_w, :] = left_img
        result_right[:right_h, -right_w:, :] = right_img

    left_position = abs(dw)
    right_position = left_w

    result[:, :left_position, :] = result_left[:, :left_position, :]
    result[:, right_position:, :] = result_right[:, right_position:, :]

    # tmp_dir = "./test_stitch"
    # if(not os.path.exists(tmp_dir)): 
    #     os.mkdir(tmp_dir)

    # cv2.imwrite(tmp_dir + "/result_l" + str(i) + ".png", result_left)
    # cv2.imwrite(tmp_dir + "/result_r" + str(i) + ".png", result_right)

    for j in range( left_position, right_position):
        #result[:, j, :] = (result_left[:, j, :] + result_right[:, j, :]) / 2
        result[:, j, :] = (result_left[:, j, :] * (right_position-j) + result_right[:, j, :] * (j-left_position)) / (right_position - left_position)

    if dh + shift_last_h < 0:
        shift_last_hh = 0
    else:
        shift_last_hh = dh + shift_last_h

    return result, shift_last_hh
