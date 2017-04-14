import cv2
# import gdfmm
import sys
import numpy as np

def voxelGridFilter(points, tcoords, gridsize=0.01):
	voxels = {}
	print len(points)
	maxX, maxY, minX, minY = -sys.maxint - 1, -sys.maxint - 1, sys.maxint, sys.maxint
	for i in range(len(points)):
		n = tuple(map(lambda x: int(round(x / gridsize)),np.copy(points[i]))[0:2])
		if n not in voxels:
			voxels[n] = []
			minX, maxX = min(n[0], minX), max(n[0], maxX)
			minY, maxY = min(n[1], minY), max(n[1], maxY)
		voxels[n].append({
			"p" : points[i],
			"t" : tcoords[i]
			})
	mask = np.zeros((3 + maxX - minX, 3 + maxY - minY), dtype=np.uint8)
	offset = (1 - minX, 1 - minY)
	for k in voxels.keys():
		mask[tuple(np.array(k) + offset)] = 255
	edge = mask - cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)))
	it = np.nditer(edge, flags=['multi_index'])
	while not it.finished:
		if it[0] == 0:
			pass
			it.iternext()
			continue
		point = tuple(np.array(it.multi_index) - offset)
		v = voxels[point]
		q1, q2, q3, q4 = [], [], [], []
		for e in v:
			((q1 if e["p"][0] > point[0] * gridsize else q2)
			     if e["p"][1] > point[1] * gridsize else
			 (q4 if e["p"][0] > point[0] * gridsize else q3)).append(e)
		if len(q1) > 3:
			voxels[(point, 'q1')] = q1
		if len(q2) > 3:
			voxels[(point, 'q2')] = q2
		if len(q3) > 3:
			voxels[(point, 'q3')] = q3
		if len(q4) > 3:
			voxels[(point, 'q4')] = q4
		del voxels[point]
		it.iternext()
	rp = [np.average(np.array([e["p"] for e in voxels[n]]), axis=0) for n in voxels]
	rt = [np.average(np.array([e["t"] for e in voxels[n]]), axis=0) for n in voxels]
	return rp, rt

def inpaint(bgr, depth):
    pass

# def inpaint(bgr, depth):
#     bgrSmall = cv2.resize(bgr, (depth.shape[1], depth.shape[0]))
#     rgb = cv2.cvtColor(bgrSmall, cv2.COLOR_BGR2RGB)
#     # pass by reference
#     depth[:] = gdfmm.InpaintDepth2(depth, rgb, 1, 1, 2.0, 11)[:]
