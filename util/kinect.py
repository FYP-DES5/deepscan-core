# import freenect
import numpy as np
import cv2
import denoise

#__ctx = freenect.init()
#__dev = freenect.open_device(__ctx, 0)
__version = None
__v2 = {}

def init(version):
    global __version
    global __v2
    __version = version
    if __version == 'v1':
        import freenect
        getVideo()
    elif __version == 'v2':
        from pylibfreenect2 import Freenect2, SyncMultiFrameListener
        from pylibfreenect2 import FrameType, Registration, Frame

        __v2["fn"] = Freenect2()
        num_devices = __v2["fn"].enumerateDevices()
        if num_devices == 0:
            print("No device connected!")
            sys.exit(1)
        __v2["serial"] = __v2["fn"].getDeviceSerialNumber(0)
        try:
            from pylibfreenect2 import OpenCLPacketPipeline
            __v2["pipeline"] = OpenCLPacketPipeline()
        except:
            from pylibfreenect2 import CpuPacketPipeline
            __v2["pipeline"] = CpuPacketPipeline()
        __v2["device"] = __v2["fn"].openDevice(__v2["serial"], pipeline=__v2["pipeline"])

        __v2["listener"] = SyncMultiFrameListener(
            FrameType.Color | FrameType.Ir | FrameType.Depth)


        # Register listeners
        __v2["device"].setColorFrameListener(__v2["listener"])
        __v2["device"].setIrAndDepthFrameListener(__v2["listener"])
        __v2["device"].start()

def getRegister(zeroImage, blurValue = 5, threshold = 3):
    from pylibfreenect2 import Freenect2, SyncMultiFrameListener
    from pylibfreenect2 import FrameType, Registration, Frame
    global __v2
    undistorted = Frame(512, 424, 4)
    registered = Frame(512, 424, 4)
    color_depth_map = np.zeros((424*512,), dtype=np.int32)
    __v2["frames"] = __v2["listener"].waitForNewFrame()
    color = np.copy(__v2["frames"]["color"].asarray())
    depth = np.copy(__v2["frames"]["depth"].asarray())
    denoise.inpaint(color, depth)
    registration = Registration(__v2["device"].getIrCameraParams(),
        __v2["device"].getColorCameraParams())
    registration.apply(__v2["frames"]["color"], __v2["frames"]["depth"],
        undistorted, registered,
        color_depth_map=color_depth_map)
    diff = np.zeros(color.shape[0:2], dtype=np.int16) + cv2.cvtColor(color, cv2.COLOR_BGR2GRAY) - cv2.cvtColor(zeroImage, cv2.COLOR_BGR2GRAY)
    diff = np.absolute(diff)
    diff = np.array(diff, dtype=np.uint8)
    avg = np.average(diff)
    print avg
    ret, mask = cv2.threshold(diff, avg, 255, cv2.THRESH_BINARY)
    # points = [None] * (512 * 424)
    points = []
    tcoords = []
    def registerPoint(i, j, colorId):
        point = registration.getPointXYZ(undistorted, i, j)
        x, y = colorId % 1920, colorId / 1920
        tcoord = (x / 1920.0, 1 - y / 1080.0)
        points.append(point)
        tcoords.append(tcoord)
    kernel = np.ones((3, 3), dtype=np.uint8)
    cv2.erode(mask, kernel, mask, iterations=3)
    cv2.dilate(mask, kernel, mask, iterations=6)
    cv2.erode(mask, kernel, mask, iterations=3)
    for i in range(424):
        for j in range(512):
            colorId = color_depth_map[512 * i + j]
            if mask[i][j] == 255 and colorId != -1:
                registerPoint(i, j, colorId)
    points, tcoords = denoise.voxelDownsample(points, tcoords)
    __v2["listener"].release(__v2["frames"])
    return color, points, tcoords


def getVideo(rot90=0):
    global __version
    global __v2
    if __version == 'v1':
        image = freenect.sync_get_video(format=freenect.VIDEO_RGB)[0]
    elif __version == 'v2':
        __v2["frames"] = __v2["listener"].waitForNewFrame()
        image = np.copy(__v2["frames"]["color"].asarray())
        import cv2
        print str(cv2.imwrite('/Users/admin/Desktop/test.png', image))
        __v2["listener"].release(__v2["frames"])
    return np.rot90(image, k=rot90)

def getDepth(rot90=0):
    global __version
    global __v2
    if __version == 'v1':
        image = freenect.sync_get_depth(format=freenect_DEPTH_11BIT)[0]
    elif __version == 'v2':
        __v2["frames"] = __v2["listener"].waitForNewFrame()
        image = __v2["frames"]["depth"].asarray()
        __v2["listener"].release(__v2["frames"])
    return np.rot90(image, k=rot90)

def getIr(rot90=0):
    global __version
    global __v2
    if __version == 'v1':
        image = freenect.sync_get_video(format=freenect.VIDEO_IR_10BIT)[0]
    elif __version == 'v2':
        __v2["frames"] = __v2["listener"].waitForNewFrame()
        image = __v2["frames"]["ir"].asarray()
        __v2["listener"].release(__v2["frames"])
    return np.rot90(image, k=rot90)

def stop():
    global __version
    global __v2
    if __version == 'v1':
        freenect.close_device(__dev)
    elif __version == 'v2':
        __v2["listener"].release(__v2["frames"])
        __v2["device"].stop()
        __v2["device"].close()
