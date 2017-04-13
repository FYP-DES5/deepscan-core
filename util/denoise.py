import cv2
import gdfmm
import numpy as np

def voxelGridFilter(points, tcoords, gridsize=0.01):
	voxels = {}
	print len(points)
	for i in range(len(points)):
		n = tuple(map(lambda x: round(x / gridsize),np.copy(points[i]))[0:2])
		if n not in voxels:
			voxels[n] = []
		voxels[n].append({
			"p" : points[i],
			"t" : tcoords[i]
			})
	rp = map(lambda n: np.average(np.array(map(lambda e: e["p"], voxels[n])), axis=0), voxels)
	rt = map(lambda n: np.average(np.array(map(lambda e: e["t"], voxels[n])), axis=0), voxels)
	print len(rp)
	return rp, rt

def inpaint(bgr, depth):
    pass

# def inpaint(bgr, depth):
#     bgrSmall = cv2.resize(bgr, (depth.shape[1], depth.shape[0]))
#     rgb = cv2.cvtColor(bgrSmall, cv2.COLOR_BGR2RGB)
#     # pass by reference
#     depth[:] = gdfmm.InpaintDepth2(depth, rgb, 1, 1, 2.0, 11)[:]
