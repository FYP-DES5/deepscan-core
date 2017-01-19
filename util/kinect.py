import freenect

def getVideo():
  return freenect.sync_get_video()[0]

def getDepth():
  return freenect.sync_get_depth()[0]
