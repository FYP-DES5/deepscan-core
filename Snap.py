"""Snap 3 photos"""

from util import format, android, kinect
import time

kinect.getDepth() # to "warm up" the kinect

android.capture() # return time close to actual capture
depth = kinect.getDepth()
video = kinect.getVideo()
time.sleep(1)
img = android.fetchImage()

format.saveImage('vid.png', video, bgr=True)
format.saveImage('dep.png', depth)
format.saveImage('img.jpg', img)
