"""Snap 3 photos"""

from util import capture, format
import time

capture.warmupKinect()

img, depth, video, ir = capture.snap(3, 0)

format.saveImage('vid.png', video, bgr=True)
format.saveImage('dep.png', depth)
format.saveImage('img.jpg', img)
format.saveImage('ir.png', ir)
