# import freenect
import numpy as np
import cv2


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

def getRegister(zeroImage, blurValue = 5, threshold = 170):
    from pylibfreenect2 import Freenect2, SyncMultiFrameListener
    from pylibfreenect2 import FrameType, Registration, Frame
    global __v2
    undistorted = Frame(512, 424, 4)
    registered = Frame(512, 424, 4)
    color_depth_map = np.zeros((424*512,), dtype=np.int32)
    __v2["frames"] = __v2["listener"].waitForNewFrame()
    color = np.copy(__v2["frames"]["color"].asarray())
    arr = __v2["frames"]["depth"].asarray()
    cv2.medianBlur(arr, blurValue, arr)
    registration = Registration(__v2["device"].getIrCameraParams(),
        __v2["device"].getColorCameraParams())
    registration.apply(
            __v2["frames"]["color"], __v2["frames"]["depth"],
            undistorted, registered, color_depth_map=color_depth_map)
    __v2["listener"].release(__v2["frames"])
    # points = [None] * (512 * 424)
    points = []
    tcoords = []
    diffPoints = np.zeros_like(color_depth_map, dtype=np.uint8)
    diff = np.zeros_like((424, 512), dtype=int)
    mapping = np.zeros((424, 512, 2), dtype=int)
    for i in range(424):
        for j in range(512):
            colorId = color_depth_map[512 * i + j]
            x = colorId % 1920
            y = colorId / 1920
            if colorId == -1:
                continue
            mapping[i][j] = y, x
            difference = np.linalg.norm(np.zeros_like(color[y][x], dtype=float)
                    + color[y][x] - zeroImage[y][x])
            diff[i][j] = difference
            if not difference > threshold:
                continue
            diffPoints[i][j] = 255
    kernel = np.ones((3, 3), dtype=np.uint8)
    numpy.savetxt('diffPoints.txt', diffPoints)
    numpy.savetxt('diff.txt', diff)
    cv2.erode(diff, kernel, iterations=3)
    cv2.dilate(diff, kernel, iterations=6)
    cv2.erode(diff, kernel, iterations=3)
    numpy.savetxt('diffPoints_after.txt', diffPoints)
    counter = 0
    for i in range(424):
        for j in range(512):
            if diffPoints[i][j] == 255:
                point = registration.getPointXYZ(undistorted, i, j)
                tcoord = (x / 1920.0, 1 - y / 1080.0)
                points.append(point)
                tcoords.append(tcoord)
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
