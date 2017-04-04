import plotly.plotly as py
from plotly.graph_objs import *

import numpy as np
import matplotlib.cm as cm
from scipy.spatial import Delaunay

u=np.linspace(0,2*np.pi, 24)
v=np.linspace(-1,1, 8)
u,v=np.meshgrid(u,v)
u=u.flatten()
v=v.flatten()

#evaluate the parameterization at the flattened u and v
tp=1+0.5*v*np.cos(u/2.)
x=tp*np.cos(u)
y=tp*np.sin(u)
z=0.5*v*np.sin(u/2.)

#define 2D points, as input data for the Delaunay triangulation of U
points2D=np.vstack([u,v]).T
tri = Delaunay(points2D)#triangulate the rectangle U
