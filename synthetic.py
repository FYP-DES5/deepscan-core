from __future__ import print_function
import numpy as np
LA = np.linalg
import lsmr as spla
import vtk

def genArrays(width, depth, maxHeight):
    points = np.zeros((width+1, depth+1, 3))
    lastx, lastz, length = 0.0, 0.0, 0.0
    for i in range(width + 1):
        x, z = i * 1.0 / width, -((i % (width / 2.0) - width / 4.0) ** 2.0) / (width / 4.0) ** 2.0 * maxHeight + maxHeight
        for j in range(depth + 1):
            y = j * 1.0 / depth
            points[i][j] = (x, y, z)
        length += ((lastx - x) ** 2 + (lastz - z) ** 2) ** .5
        lastx, lastz = x, z
    points = np.reshape(points, ((width + 1) * (depth + 1), 3))
    triangles = np.zeros((width, depth, 2, 3), int)
    for i in range(width):
        for j in range(depth):
            triangles[i][j][0][0] = (depth + 1) * i + j
            triangles[i][j][0][1] = (depth + 1) * i + j + 1
            triangles[i][j][0][2] = (depth + 1) * (i + 1) + j
            triangles[i][j][1][0] = (depth + 1) * (i + 1) + j
            triangles[i][j][1][1] = (depth + 1) * i + j + 1
            triangles[i][j][1][2] = (depth + 1) * (i + 1) + j + 1
    triangles = np.reshape(triangles, (width * depth * 2, 3))
    return points, triangles, length
def genPoints(pointsArr, maxHeight):
    points = vtk.vtkPoints()
    points.SetNumberOfPoints(pointsArr.shape[0])
    lastx, lastz, length = 0.0, 0.0, 0.0
    for i in range(pointsArr.shape[0]):
        points.SetPoint(i, pointsArr[i])
    return points
def alterPoints(points, newPoints):
    for i in range(len(newPoints)):
        points.SetPoint(i, [newPoints[i][0], newPoints[i][1], 0])
    points.Modified()
def genPolys(triangles):
    polys = vtk.vtkCellArray()
    polys.SetNumberOfCells(triangles.shape[0])
    for i in range(triangles.shape[0]):
        ids = vtk.vtkIdList()
        ids.SetNumberOfIds(3)
        for j in range(3):
            ids.SetId(j, triangles[i][j])
        polys.InsertNextCell(ids)
    return polys
def genTcoords(width, depth, arclength):
    tc = vtk.vtkFloatArray()
    tc.SetNumberOfComponents(2)
    lastx, lastz, length = 0.0, 0.0, 0.0
    for i in range(width + 1):
        x, z = i * 1.0 / width, -((i % (width / 2.0) - width / 4.0) ** 2.0) / (width / 4.0) ** 2.0 * maxHeight + maxHeight
        length += ((lastx - x) ** 2 + (lastz - z) ** 2) ** .5
        lerpAmount = length / arclength
        lastx, lastz = x, z
        for j in range(depth + 1):
            y = j * 1.0 / depth
            tc.InsertTuple2((depth + 1) * i + j, lerpAmount, y)
    return tc
def genReader(filename):
    reader = vtk.vtkPNGReader()
    reader.SetFileName(filename)
    return reader
def genTexture(reader):
    texture = vtk.vtkTexture()
    texture.SetInputConnection(reader.GetOutputPort())
    return texture
def genPolyData(points, polys, tcoords):
    pd = vtk.vtkPolyData()
    pd.SetPoints(points)
    pd.SetPolys(polys)
    pd.GetPointData().SetTCoords(tcoords)
    return pd
def genMap(polyData):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)
    return mapper
def genActor(mapper, texture):
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)
    return actor
def genRendererWindow(actor):
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    ren.AddActor(actor)
    ren.SetBackground(1, 1, 1)
    renWin.SetSize(500, 500)
    renWin.Render()
    # cam1 = ren.GetActiveCamera()
    # cam1.Zoom(1.5)
    iren.Initialize()
    # renWin.Render()
    return ren, renWin, iren
def screenshot(renWin, filename):
    filter = vtk.vtkWindowToImageFilter()
    filter.SetInput(renWin)
    filter.SetInputBufferTypeToRGBA()
    filter.Update()
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(filename)
    writer.SetInputConnection(filter.GetOutputPort())
    writer.Write()
def collectDisplayPoints(ren, renWin, points):
    num = points.GetNumberOfPoints()
    displayPoints = []
    for i in range(num):
        point = points.GetPoint(i)
        ren.SetWorldPoint(point[0], point[1], point[2], 1)
        ren.WorldToDisplay()
        dispPt = ren.GetDisplayPoint()
        displayPoints.append(dispPt)
    return displayPoints
def genNewTcoords(displayPoints):
    tc = vtk.vtkFloatArray()
    tc.SetNumberOfComponents(2)
    for i in range(len(displayPoints)):
        tc.InsertTuple2(i, displayPoints[i][0] / 500, displayPoints[i][1] / 500)
    return tc
def alterActor(actor, texture):
    actor.SetTexture(texture)
def conformalGenAB(points, triangles, fixed):
    def normal(va, vb):
        """va, vb, return : R3"""
        vn = np.cross(va, vb)
        return vn / LA.norm(vn)
    def triangleArea(va, vb):
        """va, vb: R2 or R3; return: sq. unit"""
        ab = LA.norm(va) * LA.norm(vb)
        theta = np.arccos(np.dot(va, vb) / ab)
        return ab * np.sin(theta) / 2
    def basisChange(p1, p2, p3):
        """R3 -> R2; the returned p1 is always (0, 0)"""
        va, vb = p2 - p1, p3 - p1
        vn = normal(va, vb)
        vx = normal(vn, vb)
        vy = normal(vx, vn)
        p1 = np.array([0, 0])
        p2 = np.array([np.dot(va, vx), np.dot(va, vy)])
        p3 = np.array([np.dot(vb, vx), np.dot(vb, vy)])
        return p1, p2, p3
    def genSubmatrix(p1, p2, p3):
        """p1, p2, p3: R2, return: 2*6 matrix"""
        at = triangleArea(p2 - p1, p3 - p1)
        rowX, rowY = np.transpose(np.array([p3 - p2, p1 - p3, p2 - p1]))
        sub = np.vstack([np.hstack([rowX, -rowY]),
                         np.hstack([rowY, rowX])])
        sub /= 2 * at
        return sub
    pn, tn = len(points), len(triangles)
    a = np.zeros((tn * 2, pn * 2))
    for i in range(len(triangles)):
        i1, i2, i3 = triangles[i]
        p1, p2, p3 = points[i1], points[i2], points[i3]
        p1, p2, p3 = basisChange(p1, p2, p3)
        submatrix = genSubmatrix(p1, p2, p3)
        r, c = [i, i + tn], [i1, i2, i3, i1 + pn, i2 + pn, i3 + pn]
        for ri in range(len(r)):
            for ci in range(len(c)):
                a[r[ri]][c[ci]] = submatrix[ri][ci]
    fixedIndexes = fixed.T[0]
    slices = np.vstack([fixedIndexes, fixedIndexes + 1]).T.flatten()
    slices = np.hstack([slices, slices + pn])
    a = np.hsplit(a, slices)
    b = -np.dot(np.hstack([a[i] for i in range(len(a)) if i % 2]),
                 np.hsplit(fixed, [1])[1].T.flatten())
    a = np.hstack([a[i] for i in range(len(a)) if not i % 2])
    return a, b
def solveSparse(a, b, xest=None):
    # x, residuals, rank, s = LA.lstsq(a, b)
    x, istop, itn, normr, normar, normA, condA, normx, xarr = spla.lsmr(a, b, xest=xest)
    return x, xarr
def xToPoints(x, fixed):
    fixedIndexes = fixed.T[0]
    fixedPoints = np.hsplit(fixed, [1])[1]
    newPoints = np.vstack(np.hsplit(x, 2)).T
    newPoints = np.vsplit(newPoints, fixedIndexes - np.arange(len(fixedIndexes)))
    newPoints = np.vstack([(fixedPoints[i / 2] if i % 2
        else newPoints[i / 2])
        for i in range(len(newPoints) * 2 - 1)])
    return newPoints

maxHeight, width, depth = 0.2, 40, 40
ptArray, triArray, arclength = genArrays(width, depth, maxHeight)
points = genPoints(ptArray, maxHeight)
polys = genPolys(triArray)
tcoords = genTcoords(width, depth, arclength)
reader = genReader('custom1.png')
texture = genTexture(reader)
polyData = genPolyData(points, polys, tcoords)
mapper = genMap(polyData)
actor = genActor(mapper, texture)
ren, renWin, iren = genRendererWindow(actor)
if True: # blocking, let user fiddle with angles / wireframe
    iren.Start()
displayPoints = collectDisplayPoints(ren, renWin, points)
screenshot(renWin, 'screenshot.png')
if False: # switch with screenshot
    reader = genReader('screenshot.png')
    texture = genTexture(reader)
    tcoords = genNewTcoords(displayPoints)
    polyData.GetPointData().SetTCoords(tcoords)
    alterActor(actor, texture)
if True: # does conformal mapping
    fixed = np.array([[0, 0, 0],
                      #[40, 0, 1],
                      #[len(ptArray) - 41, 1, 0],
                      [len(ptArray) - 1, 1, 1]])
    a, b = conformalGenAB(ptArray, triArray, fixed)
    print('solving Ax=B problem..')
    x, xarr = solveSparse(a, b)
    print('number of iterations:', len(xarr))
    if True: # show animation
        for i in range(len(xarr)):
            newPoints = xToPoints(xarr[i], fixed)
            alterPoints(points, newPoints)
            renWin.Render()
            if False:
                # save file
                screenshot(renWin, 'result-%03d.png' % i)
    newPoints = xToPoints(x, fixed)
    alterPoints(points, newPoints)
renWin.Render()
iren.Start()
screenshot(renWin, 'result.png')
