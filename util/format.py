import sys
import cv2
import pickle
import numpy as np

def saveImage(name, img, bgr=False):
  if len(img.shape) == 2:
    img = np.vectorize(lambda x: x / 8)(img) # downgrade
    img = np.dstack((img, img, img)) # K -> KKK
  elif bgr:
    img = img[:, :, [2, 1, 0]] # BGR -> RGB
  cv2.imwrite(name, img)

