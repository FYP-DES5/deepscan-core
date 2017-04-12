import cv2
import gdfmm

def voxelDownsample(points, tcoords):
    return points, tcoords

def inpaint(bgr, depth):
    pass

# def inpaint(bgr, depth):
#     bgrSmall = cv2.resize(bgr, (depth.shape[1], depth.shape[0]))
#     rgb = cv2.cvtColor(bgrSmall, cv2.COLOR_BGR2RGB)
#     # pass by reference
#     depth[:] = gdfmm.InpaintDepth2(depth, rgb, 1, 1, 2.0, 11)[:]
