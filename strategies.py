import cv2 

import numpy as np 
import operator as op 
import itertools as it, functools as ft 

def read_image(path2image, size=None):
    image = cv2.imread(path2image, cv2.IMREAD_COLOR)
    if size is not None:
        image = cv2.resize(image, size, cv2.INTER_CUBIC)
    return image 
