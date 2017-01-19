#!/usr/bin/python

import sys
import cv2
import pickle
import numpy as np

arr = pickle.load(open(sys.argv[-1], "r"))
if len(arr.shape) == 2:
  arr = np.vectorize(lambda x: x / 8)(arr)
  arr = np.dstack((arr, arr, arr))
else:
  arr = arr[:, :, [2, 1, 0]]
cv2.imwrite(sys.argv[-1] + "ng", arr)
