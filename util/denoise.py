import numpy as np
import cv2

def medianBlur(src):
    return cv2.medianBlur(src, 5)
