import numpy as np
import cv2
import glob
from math import sqrt

print("Initialising...")

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

cellSize = 28
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)*cellSize

# Arrays to store object points and image points from all the images.
objectPoints = [] # 3d point in real world space
imagePointsLeft = [] # 2d points in image plane.
imagePointsRight = []

capLeft  = cv2.VideoCapture(0)
capRight = cv2.VideoCapture(1)

count = 50;

print("Collecting data...")
print(count)
while(capLeft.isOpened() and capRight.isOpened()):
	while(count > 0):
		# Capture frame-by-frame
        	ret, imageLeft  = capLeft.read()
        	ret, imageRight = capRight.read()

		greyLeft  = cv2.cvtColor(imageLeft,cv2.COLOR_BGR2GRAY)
		greyRight = cv2.cvtColor(imageRight,cv2.COLOR_BGR2GRAY)
#		cv2.imshow('img',greyLeft)

		# Find the chess board corners
		retLeft,  cornersLeft  = cv2.findChessboardCorners(greyLeft, (9,6),None)
		#retRight, cornersRight = cv2.findChessboardCorners(greyRight, (9,6),None)

		quickTest = False

		# If found, add object points, image points (after refining them)
		if retLeft == True:

			cornersLeft2 = cv2.cornerSubPix(greyLeft,cornersLeft,(11,11),(-1,-1),criteria)

			# Draw and display the corners
			imageLeft = cv2.drawChessboardCorners(imageLeft, (9,6), cornersLeft2, retLeft)
			rect = cv2.minAreaRect(cornersLeft2)
	    		box = cv2.boxPoints(rect)
	    		box2 = np.int0(box)

		        size  = rect[1]
		        area  = size[0]*size[1]


			first = cornersLeft2[0,0]
			delta = 100000
			horizontal = None
			angle = abs(rect[2])
			for i in range(4):
				point = box[i]
				x1 = abs(first[0] - point[0])
				y1 = abs(first[1] - point[1])
				delta1 = sqrt(x1*x1+y1*y1)
				if delta1 < delta:
					if i == 0:
		                                if 0 <= angle < 45:
		                                        horizontal = False
		                                else:
			                                horizontal = True
						ratio = size[0]/size[1]
					elif i == 1:
						if 0 <= angle < 45:
							horizontal = True
						else:
							horizontal = False
						ratio = size[1]/size[0]
					elif i == 2:
						if 0 <= angle < 45:
		                                        horizontal = False
		                                else:
		                                        horizontal = True
						ratio = size[0]/size[1]
		                        elif i == 3:
		                                if 0 <= angle < 45:
		                                        horizontal = True
		                                else:
		                                        horizontal = False
						ratio = size[1]/size[0]

					delta = delta1
			print(horizontal,ratio)
			if area >= 20000:
	#			if horizontal == True and 0.35 <= ratio <= 1:
	#				quickTest = True
	#			elif horizontal == False and 0.35 <= ratio <= 1:
				if 0.4 <= ratio <= 1:
					quickTest = True
			print(quickTest)

			if quickTest == True:
			        imagePointsLeft.append(cornersLeft2)
			        objectPoints.append(objp)
	    			cv2.drawContours(imageLeft,[box2],0,(0,255,0),2)
				count = count - 1
				print(count)
			else:
				cv2.drawContours(imageLeft,[box2],0,(0,0,255),2)

		cv2.imshow('img',imageLeft)

		if cv2.waitKey(50) & 0xFF == ord('q'):
			break
	print("Data collected...")
	break
# When everything done, release the capture
capLeft.release()
capRight.release()
cv2.destroyAllWindows()

