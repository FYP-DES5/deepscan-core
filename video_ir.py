from util import kinect, format
import cv2
import freenect
import numpy as np

while 1:
  img = kinect.getIr()
  print img
  cv2.imshow('ir', img)
  if cv2.waitKey(10) == 27:
    break
