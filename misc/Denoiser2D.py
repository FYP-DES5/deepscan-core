import numpy as np
import cv2

img = cv2.imread('check_video.png')

dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

cv2.imshow('before', img)
cv2.imshow('after', dst)
cv2.waitKey(0)
