# Python script for png

import numpy as np
import helpers
import cv2

def is_sensitive(filename, detector):
    small_threshold = 0.3
    abs_threshold = 0.5
    imgArr = cv2.imread(str(filename))
    background = np.array([255, 255, 255])

    percent = (imgArr == background).sum() / imgArr.size

    if percent >= abs_threshold:
        return True
    if percent >= small_threshold:
        return "Review"
    else:
        return False 
    
