import cv2
import gdfmm

def inpaint(bgr, depth):
    cv2.resize(rgb, depth.shape[0:2], rgb)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    # pass by reference
    depth[:] = gdfmm.InpaintDepth2(depth, rgb, 1, 1, 2.0, 11)[:]
