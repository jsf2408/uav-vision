import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objectPoints = [] # 3d point in real world space
imagePointsLeft = [] # 2d points in image plane.
imagePointsRight = []

capLeft  = cv2.VideoCapture(0)
capRight = cv2.VideoCapture(1)

while(capLeft.isOpened() and capRight.isOpened()):
# Capture frame-by-frame
        ret, imageLeft  = capLeft.read()
        ret, imageRight = capRight.read()

	greyLeft  = cv2.cvtColor(imageLeft,cv2.COLOR_BGR2GRAY)
	greyRight = cv2.cvtColor(imageRight,cv2.COLOR_BGR2GRAY)
	cv2.imshow('img',greyLeft)

	# Find the chess board corners
	ret, cornersLeft = cv2.findChessboardCorners(greyLeft, (9,6),None)
	ret, cornersLeft = cv2.findChessboardCorners(greyLeft, (9,6),None)

	# If found, add object points, image points (after refining them)
	if ret == True:
        	objectPoints.append(objp)

        	corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        	imgpoints.append(corners2)

        	# Draw and display the corners
        	img = cv2.drawChessboardCorners(img, (9,6), corners2,ret)
        	cv2.imshow('img',img)
        cv2.waitKey(500)
