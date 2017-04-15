import cv2
# import gdfmm
import sys
import numpy as np

class EdgeImprover:
	def __init__(self, voxels, gridsize, minX, minY, maxX, maxY):
		self.voxels = voxels
		self.gridsize = gridsize
		self.mask = np.zeros((3 + maxX - minX, 3 + maxY - minY), dtype=np.uint8)
		self.offset = (1 - minX, 1 - minY)
		for k in self.voxels.keys():
			self.mask[tuple(np.array(k) + self.offset)] = 255
		self.edge = self.mask - cv2.erode(self.mask, cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)))
		self.toBeDeleted = []
	def run(self):
		it = np.nditer(self.edge, flags=['multi_index'])
		frequencies = {}
		while not it.finished:
			if it[0] != 0:
				it.iternext()
				continue
			point = tuple(np.array(it.multi_index) - offset)
			frequency = len(voxels[point])
			frequencies[frequency] = 1 + frequencies.get(frequency, 0)
			it.iternext()
		modeGridPoints = max(frequencies, key=lambda k: frequencies[k])
		it = np.nditer(edge, flags=['multi_index'])
		while not it.finished:
			if it[0] == 0:
				it.iternext()
				continue
			point = tuple(np.array(it.multi_index) - offset)
			points = self.__getNeighborhoodPoints(self.voxels, point)
			centroid, ns = self.__fitPointsToPlanes(points)
			center = np.array(point, dtype=np.float64) * gridsize
			targetAreaRatio = len(voxels[point]) / float(modeGridPoints)
			xy = self.__calculateBestSample(center, centroid, gridsize, targetAreaRatio)
			voxels[(x, 'calibrated')] = self.__genVFromXYNNN(xy[0], xy[1], ns)
			self.toBeDeleted.append(point)
			it.iternext()
		for x in toBeDeleted:
			del self.voxels[x]
	@staticmethod
	def __getNeighborhoodPoints(voxels, x, y):
		return sum([[] if (i, j) not in voxels else voxels[(i, j)]
						for i in range(x - 1, x + 2)
						for j in range(y - 1, y + 2)],
				   [])
	@staticmethod
	def __genVFromXYNNN(x, y, ns):
		v = np.array([x, y, 0, 0, 0])
		for i in range(2, 5):
			n = ns[i - 2]
			v[i] = -np.dot(v[(0, 1)], n[(0, 1)]) / n[2]
		return v
	@staticmethod
	def __fitPointsToPlanes(points):
		if type(points) is not np.ndarray:
			points = np.array(points)
		centroid = np.average(points, axis=0)
		pointsRelativeToCentroid = points - centroid
		timesTable = np.dot(pointsRelativeToCentroid.T, pointsRelativeToCentroid)
		def getNormal(n):
			D = np.linalg.det(timesTable[0:2, 0:2])
			a = np.linalg.det(timesTable[0:2, (1,n)]) / D
			b = -np.linalg.det(timesTable[(0,n), 0:2]) / D
			return np.array([a, b, 1])
		return centroid, map(getNormal, range(2, 5))
	@staticmethod
	def __calculateBestSample(center, centroid, gridsize, targetAreaRatio):
		# const center, const centroid
		center = np.copy(center)
		centroid = np.copy(centroid[[0, 1]])

		d = center - centroid
		# if ratio is more than half
		if targetAreaRatio > 0.5:
			# equivalent to reversing direction and finding complement
			d = -d
			centroid = centroid + d
			targetAreaRatio = 1 - targetAreaRatio
		# if horizontal d
		if abs(d[0]) > abs(d[1]):
			# swap x and y of input
			center[[0, 1]] = center[[1, 0]]
			centroid[[0, 1]] = centroid[[1, 0]]
			yx = __calculateBestSample(center, centroid, gridsize, targetAreaRatio)
			# swap x and y of output
			return yx[[1, 0]]
		# if centroid is above
		if d[1] < 0:
			# reflect y of input
			center[1] = -center[1]
			centroid[1] = -centroid[1]
			x_negY = __calculateBestSample(center, centroid, gridsize, targetAreaRatio)
			# reflect y of output
			return x_negY * [1, -1]
		# if centroid is to the right
		if d[0] < 0:
			# reflect y of input
			center[0] = -center[0]
			centroid[0] = -centroid[0]
			negX_y = __calculateBestSample(center, centroid, gridsize, targetAreaRatio)
			# reflect y of output
			return negX_y * [-1, 1]
		# valid assumption: centroid is between S45W and S, ratio <= 0.5

		halfGrid = gridsize / 2.0
		# m = dy / dx
		md = d[1] / d[0]
		# mx + c = y
		#      c = y - mx
		cd = center[1] - md * center[0]

		# `y = h` is a line cutting square in targetAreaRatio
		h = gridsize * targetAreaRatio + center[1] - halfGrid

		# `y = mx + c` is a line cutting square in targetAreaRatio
		# and perpendicular to center - centroid
		m1 = -(d[0] / d[1])
		# mx + c = y
		#      c = y - mx
		c1 = h - m1 * center[0]

		# test if `y = mx + c` touches the left and right edge of the square
		leftY = m1 * (center[0] - halfGrid) + c1
		rightY = m1 * (center[0] + halfGrid) + c1
		if all(map(lambda y: center[1] - halfGrid < y < center[1] + halfGrid,
		           [leftY, rightY])):
			#                -m1x + y = c1
			#                -mdx + y = cd
			# -> [-m1 1; -md 1][x; y] = [c1; cd]
			return np.linalg.solve([[-m1, 1], [-md, 1]], [c1, cd])
		else:
			# area must be triangular
			# let base be bt, height be ht
			# area = bt ht / 2
			#   md = bt / ht
			# area = md / 2 * ht^2
			#   ht = sqrt(2area / md)
			m2 = m1
			# mx + c = y
			#      c = y - mx
			ht = np.sqrt(2 * targetAreaRatio * gridsize**2 / md)
			yt = ht + center[1] - halfGrid
			c2 = yt - m2 * (center[0] - halfGrid)
			xy = np.linalg.solve([[-m2, 1], [-md, 1]], [c2, cd])
			# check if in range
			if not xy[1] < center[1] - halfGrid:
				return xy
			else:
				# triangle too small, point outside of square
				# compromise: return closest point on line
				bt = md * ht
				xt = bt + center[0] - halfGrid
				return np.array([xt, center[1] - halfGrid])

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
		voxels[n].append(np.hstack((points[i], tcoords[i])))
	EdgeImprover(voxels, gridsize, minX, minY, maxX, maxY).run()
	rp = [np.average(np.array([e[0:3] for e in voxels[n]]), axis=0) for n in voxels]
	rt = [np.average(np.array([e[3:5] for e in voxels[n]]), axis=0) for n in voxels]
	return rp, rt

def inpaint(bgr, depth):
    pass

# def inpaint(bgr, depth):
#     bgrSmall = cv2.resize(bgr, (depth.shape[1], depth.shape[0]))
#     rgb = cv2.cvtColor(bgrSmall, cv2.COLOR_BGR2RGB)
#     # pass by reference
#     depth[:] = gdfmm.InpaintDepth2(depth, rgb, 1, 1, 2.0, 11)[:]
