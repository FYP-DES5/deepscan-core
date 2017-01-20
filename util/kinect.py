import freenect
import numpy as np

#__ctx = freenect.init()
#__dev = freenect.open_device(__ctx, 0)

def getVideo(rot90=0, format=0):
  image = freenect.sync_get_video(format=format)[0]
  return np.rot90(image, k=rot90)

def getDepth(rot90=0, format=0):
  image = freenect.sync_get_depth(format=format)[0]
  return np.rot90(image, k=rot90)

def stop():
  freenect.close_device(__dev)
