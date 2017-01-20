import sys
import cv2
import pickle
import numpy as np

def saveImage(name, img, bgr=False, verbose=False):
  if len(img.shape) == 2:
    if img.dtype == 'uint16':
      img = np.vectorize(lambda x: x / 8)(img) # downgrade if it is the 11bit format
    img = np.dstack((img, img, img)) # K -> KKK
  elif bgr:
    img = bgrToRgb(img)
  cv2.imwrite(name, img)
  if verbose:
    print 'Saved %s.' % name

def bgrToRgb(img):
  return img[:, :, [2, 1, 0]]
