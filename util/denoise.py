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
	mask = np.zeros((2 + maxX - minX, 2 + maxY - minY), dtype=np.uint8)
	mask[np.array(voxels.keys()) + (1 - minX, 1 - minY)] = 255
	contours, hierachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	largestContour = max(contours, key=cv2.contourArea)
	targetPoints = int(round(8 * len(voxels) ** 0.5))
	contourPoints = []
	for i in range(len(largestContour)):
		p1 = largestContour[i - 1][0]
		p2 = largestContour[i][0]
		diff = p2 - p1
		mag = max(*[abs(n) for n in diff])
		step = np.array(diff) / mag
		for j in range(mag):
			contourPoints.append(tuple(p1 + diff * j))
	for point in contourPoints:
		v = voxels[point]
		q1, q2, q3, q4 = [], [], [], []
		for e in v:
			((q1 if e["p"][0] > point[0] else q2)
				if e["p"][1] > point[1] else
			 (q4 if e["p"][0] > point[0] else q3)).append(e)
		if len(q1) > 0:
			voxels[(point, 'q1')] = q1
		if len(q2) > 0:
			voxels[(point, 'q2')] = q2
		if len(q3) > 0:
			voxels[(point, 'q3')] = q3
		if len(q4) > 0:
			voxels[(point, 'q4')] = q4
		del voxels[point]
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
