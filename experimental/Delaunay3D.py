from numpy import random
import vtk

# The points to be triangulated are generated randomly in the unit
# cube located at the origin. The points are then associated with a
# vtkPolyData.
math = vtk.vtkMath()
points = vtk.vtkPoints()

i = 0
maxHeight = 0.2
width = 150
depth = 50
for x in range(width):
    for y in range(depth):
        points.InsertPoint(i, x * 1.0 / width, y * 1.0 / depth, -((x % (width / 2) - width / 4) ** 2) / (width / 4.0) ** 2 * maxHeight + maxHeight)
        i += 1

# math = vtk.vtkMath()
# points = vtk.vtkPoints()
# for i in range(0, 25):
#     points.InsertPoint(i, math.Random(0, 1), math.Random(0, 1),
#                        math.Random(0, 1))

profile = vtk.vtkPolyData()
profile.SetPoints(points)

# Delaunay3D is used to triangulate the points. The Tolerance is the
# distance that nearly coincident points are merged
# together. (Delaunay does better if points are well spaced.) The
# alpha value is the radius of circumcircles, circumspheres. Any mesh
# entity whose circumcircle is smaller than this value is output.
delny = vtk.vtkDelaunay3D()
delny.SetInputData(profile)
delny.SetTolerance(5)
delny.SetAlpha(0.2)
delny.BoundingTriangulationOff()
delny.Update()

usg = vtk.vtkUnstructuredGrid()
usg = delny.GetOutput()
pd = vtk.vtkPolyData()

pd.SetPoints(usg.GetPoints())
pd.SetPolys(usg.GetCells())


sr = vtk.vtkSurfaceReconstructionFilter()
sr.SetNeighborhoodSize(8)
sr.SetInputData(profile)
sr.Update()

cf = vtk.vtkContourFilter()
cf.SetInputConnection(sr.GetOutputPort())
cf.SetValue(0, 0.0)


# Shrink the result to help see it better.
# shrink = vtk.vtkShrinkFilter()
# shrink.SetInputConnection(delny.GetOutputPort())
# shrink.SetShrinkFactor(1.0)

map = vtk.vtkDataSetMapper()
map.SetInputConnection(cf.GetOutputPort())

triangulation = vtk.vtkActor()
triangulation.SetMapper(map)
triangulation.GetProperty().SetColor(1, 0, 0)

# Create graphics stuff
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
ren.AddActor(triangulation)
ren.SetBackground(1, 1, 1)
renWin.SetSize(500, 500)
renWin.Render()

cam1 = ren.GetActiveCamera()
cam1.Zoom(1.5)

iren.Initialize()
renWin.Render()
iren.Start()