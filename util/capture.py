"""Input library"""

import format, android, kinect
import time

def warmupKinect():
  kinect.getDepth()

def snap(androidRotation=0, kinectRotation=0, verbose=False):
    """
    snap(androidRotation=0, kinectRotation=0, verbose=False) -> img, depth, video, ir

    Snaps and returns 4 images.
    """

    if verbose:
        print '  taking photo with phone...'
    android.capture() # return time close to actual capture
    if verbose:
        print '  taking photo with Kinect...'
    depth = kinect.getDepth(kinectRotation)
    video = kinect.getVideo(kinectRotation)
    ir = kinect.getIr(kinectRotation)
    if verbose:
        print '  sleeping for 1 second...'
    time.sleep(1) # give phone time to write to storage
    if verbose:
        print '  fetching image from phone...'
    img = android.fetchImage(androidRotation)
    return img, depth, video, ir
