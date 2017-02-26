import freenect
import numpy as np

#__ctx = freenect.init()
#__dev = freenect.open_device(__ctx, 0)
__version = None
__v2 = {}

def init(version):
  __version = version
  if __version = 'v1':
  	import freenect
  	getVideo()
  else:
  	from pylibfreenect2 import Freenect2, SyncMultiFrameListener
	from pylibfreenect2 import FrameType, Registration, Frame
  	
    __v2["fn"] = Freenect2()
    num_devices = fn.enumerateDevices()
    if num_devices == 0:
      print("No device connected!")
      sys.exit(1)
    __v2["device"] = fn.openDevice(serial, pipeline=pipeline)

    __v2["listener"] = SyncMultiFrameListener(
      FrameType.Color | FrameType.Ir | FrameType.Depth)


    # Register listeners
    __v2["device"].setColorFrameListener(listener)
    __v2["device"].setIrAndDepthFrameListener(listener)

    __v2["device"].start()



def getVideo(rot90=0):
  if __version = 'v1':
    image = freenect.sync_get_video(format=freenect.VIDEO_RGB)[0]
  else:
    __v2["frames"] = __v2["listener"].waitForNewFrame()
    image = __v2["frames"]["color"].asarray()
  return np.rot90(image, k=rot90)

def getDepth(rot90=0):
  if __version = 'v1':
    image = freenect.sync_get_depth(format=freenect_DEPTH_11BIT)[0]
  else:
    __v2["frames"] = __v2["listener"].waitForNewFrame()
    image = __v2["frames"]["depth"].asarray()
  return np.rot90(image, k=rot90)

def getIr(rot90=0):
  if __version = 'v1':
    image = freenect.sync_get_video(format=freenect.VIDEO_IR_10BIT)[0]
  else:
    __v2["frames"] = __v2["listener"].waitForNewFrame()
  	image = __v2["frames"]["ir"].asarray()
  return np.rot90(image, k=rot90)

def stop():
  if __version = 'v1':
    freenect.close_device(__dev)
  else:
    __v2["listener"].release(__v2["frames"])
    __v2["device"].stop()
    __v2["device"].close()