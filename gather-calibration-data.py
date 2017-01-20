"""Snap 3 photos"""

from util import android, capture, format
import freenect

capture.warmupKinect()

n = 0
while raw_input('Press Enter to capture next photo. Input "n" to stop.') != 'n':
  img, depth, video = capture.snap(3, 0, videoFormat=freenect.VIDEO_IR_8BIT)
  if img is not None:
    format.saveImage('vid_%03d.png' % n, video, bgr=True, verbose=True)
    format.saveImage('dep_%03d.png' % n, depth, verbose=True)
    format.saveImage('img_%03d.jpg' % n, img, verbose=True)
    n = n + 1
  else:
    print 'phone capture failed'
    android.clean()
