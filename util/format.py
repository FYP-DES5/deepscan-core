import sys
import cv2
import pickle
import os
import numpy as np

def saveImage(name, img, bgr=False, verbose=False):
    name = os.path.abspath(name)
    if verbose:
        print 'Saving %s...' % name
    if len(img.shape) == 2:
        if verbose:
            print '  BW image detected'
            print '  dtype: ' + str(img.dtype)
        if img.dtype == 'uint16':
            img = np.vectorize(lambda x: x / 8)(img) # downgrade if it is the 11bit format
        img = np.dstack((img, img, img)) # K -> KKK
    elif bgr:
        if verbose:
            print '  changing bgr to rgb'
        img = bgrToRgb(img)
    if verbose:
        print '  imwrite call'
        print img
        print 'result: ' + str(cv2.imwrite(name, img))
    else:
        cv2.imwrite(name, img)
    if verbose:
        print 'Saved %s.' % name

def bgrToRgb(img):
    if img.shape[2] is 3:
        return img[:, :, [2, 1, 0]]
    else:
        return np.dsplit(img[:, :, [2, 1, 0, 3]], (3, 1))[0]