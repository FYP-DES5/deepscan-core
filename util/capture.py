"""Input library"""

import format, android, kinect
import time

def warmupKinect():
  kinect.getDepth()

def snap(androidRotation=0, kinectRotation=0, videoFormat=0, depthFormat=0):
  """
  snap(androidRotation=0, kinectRotation=0) -> img, depth, video
  
  Snaps and returns 3 images.
  """

  android.capture() # return time close to actual capture
  depth = kinect.getDepth(kinectRotation, depthFormat)
  video = kinect.getVideo(kinectRotation, videoFormat)
  time.sleep(1) # give phone time to write to storage
  img = android.fetchImage(androidRotation)
  return img, depth, video


