from __future__ import print_function
import numpy as np
import cv2
import freenect
import glob
import sys
import os
import pickle

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# chessboardShape = (12, 12)
# images = [glob.glob('test/calibration/Left*.jpg'), glob.glob('test/calibration/Right*.jpg')]
chessboardShape = (9, 7)
images = [glob.glob('test/calibration/img_*'), glob.glob('test/calibration/vid_*')]
resize = True

objp = np.zeros((chessboardShape[1]*chessboardShape[0],3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardShape[0],0:chessboardShape[1]].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [[],[]] # camera, ir
imgpoints = [[],[]] # camera, ir
successes = [[],[]] # camera, ir
params = [{}, {}]

if os.path.isfile("calibdata.pickle"):
    load = pickle.load(open("calibdata.pickle", "r"))
    params = load["params"]
    objpoints = load["objpoints"]
    imgpoints = load["imgpoints"]
    successes = load["successes"]
    if False: # stereo calibrate ir and ir
        params[0] = params[1]
        imgpoints[0] = imgpoints[1]
        objpoints[0] = objpoints[1]
        successes[0] = successes[1]
    elif False: # stereo calibrate img and img
        params[1] = params[0]
        imgpoints[1] = imgpoints[0]
        objpoints[1] = objpoints[0]
        successes[1] = successes[0]
        #imgpoints = map(lambda x: map(lambda y: y / 10, x), imgpoints)
    else:
        pass
        #imgpoints = map(lambda x: map(lambda y: y / 2, x), imgpoints)
        #imgpoints[0] = map(lambda y: y / 2, imgpoints[0])
        #imgpoints[1] = map(lambda y: y, imgpoints[0])
        #params[1] = params[0]
else:
    for i in range(2):
        for fname in sorted(images[i]):
            img = cv2.imread(fname)
            if resize:
                print(img.shape, end="->")
                img = cv2.resize(img, (640, 480))
                print(img.shape, end=" ")
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            print(fname + ": ", end="")
            sys.stdout.flush()

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, chessboardShape, None)
            print(str(ret))

            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints[i].append(objp)

                corners2 = cv2.cornerSubPix(gray,corners,(11,11), (-1,-1),criteria)
                imgpoints[i].append(corners2)
                img = cv2.drawChessboardCorners(img, chessboardShape, corners2, ret)
                path = fname.split("/")
                path[-1] = "chess_" + path[-1]
                cv2.imwrite("/".join(path), img)
            successes[i].append(ret)

        params[i]["h"], params[i]["w"] = img.shape[:2]
        params[i]["ret"], params[i]["mtx"], params[i]["dist"], \
          params[i]["rvecs"], params[i]["tvecs"] = \
          cv2.calibrateCamera(objpoints[i], imgpoints[i], (params[i]["h"], params[i]["w"]), None, None)
        dump = {
          'params': params,
          'objpoints': objpoints,
          'imgpoints': imgpoints,
          'successes': successes
        }
        # this is just for single camera stuff
        #params[i]["newcameramtx"], params[i]["roi"] = \
        #  cv2.getOptimalNewCameraMatrix(params[i]["mtx"], params[i]["dist"], \
        #  (params[i]["w"], params[i]["h"]), 1, (params[i]["w"], params[i]["h"]))
    pickle.dump(dump, open("calibdata.pickle", "w"))

stereoObjpoints = []
stereoImgpoints = [[], []]
for i in range(len(successes[0])):
    if successes[0][i] and successes[1][i]:
        stereoObjpoints.append(objp)
        stereoImgpoints[0].append(imgpoints[0][0])
        stereoImgpoints[1].append(imgpoints[1][0])
        imgpoints[0] = imgpoints[0][1:]
        imgpoints[1] = imgpoints[1][1:]

imageSize = (params[0]["w"], params[0]["h"])

retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = \
  cv2.stereoCalibrate(stereoObjpoints, stereoImgpoints[0], stereoImgpoints[1],\
    params[0]["mtx"], params[0]["dist"], params[1]["mtx"], params[1]["dist"],\
    imageSize, criteria,\
    flags=cv2.CALIB_FIX_INTRINSIC)

R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = \
  cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R, T, alpha=0)

print(R1, R2, P1, P2, Q, validPixROI1, validPixROI2, sep="\n\n")


    #initUndistortRectifyMap(cameraMatrix[0], distCoeffs[0], R1, P1, (640, 480), CV_16SC2, rmap[0][0], rmap[0][1]);
    #initUndistortRectifyMap(cameraMatrix[1], distCoeffs[1], R2, P2, (640, 480), CV_16SC2, rmap[1][0], rmap[1][1]);

mapx1, mapy1 = cv2.initUndistortRectifyMap(params[0]["mtx"], params[0]["dist"], R1, P1, (640, 480), cv2.CV_16SC2)
mapx2, mapy2 = cv2.initUndistortRectifyMap(params[1]["mtx"], params[1]["dist"], R2, P2, (640, 480), cv2.CV_16SC2)

lolk = []
for fname in sorted(images[0]):
    img = cv2.imread(fname)
    if resize:
        img = cv2.resize(img, (640, 480))
    stuff = np.copy(img)
    img = cv2.remap(img, mapx1, mapy1, cv2.INTER_LINEAR)
    stuff = np.concatenate((stuff, img))
    lolk.append(np.copy(stuff))

i = 0
for fname in sorted(images[1]):
    img = cv2.imread(fname)
    if resize:
        img = cv2.resize(img, (640, 480))
    stuff = np.copy(img)
    img = cv2.remap(img, mapx2, mapy2, cv2.INTER_LINEAR)
    stuff = np.concatenate((stuff, img))
    img = np.concatenate((lolk[i], stuff), 1)
    path = fname.split("/")
    path[-1] = "calibrated_" + path[-1]
    cv2.imwrite("/".join(path), img)
    i = i + 1
