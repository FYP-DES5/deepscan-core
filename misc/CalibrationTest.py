import numpy as np
import cv2
import freenect

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((4*11,3), np.float32)
objp[:,:2] = np.mgrid[0:11,0:4].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


img = cv2.imread('/tmp/pattern.png')
gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

# Find the chess board corners
ret, corners = cv2.findCirclesGrid(gray, (11,4), flags=cv2.CALIB_CB_ASYMMETRIC_GRID)
print ret

# If found, add object points, image points (after refining them)
if ret == True:
    objpoints.append(objp)

    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    imgpoints.append(corners2)

    # Draw and display the corners
    img = cv2.drawChessboardCorners(img, (11,4), corners2,ret)
    cv2.imshow('img',img)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
img = cv2.imread('/tmp/pattern.png')
h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imshow('original', img)
cv2.imshow('undistorted', dst)
cv2.waitKey(0)
