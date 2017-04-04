#! /usr/local/bin/python

"""Snap 3 photos"""

from __future__ import print_function 
from util import capture, format, kinect
import time
from pylibfreenect2 import Frame, Registration
import numpy as np

kinect.init('v2')
capture.warmupKinect()

undistorted, registered, color_depth_map = kinect.getRegister()

kinect.stop()

for i in range(color_depth_map.shape[0]):
	print(color_depth_map[i], end=',')
print("")