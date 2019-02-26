import numpy as np
import cv2
import glob
from math import sqrt

def quickTest(box, size, first, rect):
        delta = 100000
        area  = size[0]*size[1]
        horizontal = None
        angle = abs(rect[2])
        for i in range(4):
                point = box[i]
                x1 = abs(first[0] - point[0])
                y1 = abs(first[1] - point[1])
                delta1 = sqrt(x1*x1+y1*y1)
                if delta1 < delta:
                        if i == 0:
#                                if 0 <= angle < 45:
#                                        horizontal = False
#                                else:
#                                       horizontal = True
                                ratio = size[0]/size[1]
                        elif i == 1:
#                               if 0 <= angle < 45:
#                                       horizontal = True
#                               else:
#                                       horizontal = False
                                ratio = size[1]/size[0]
                        elif i == 2:
#                               if 0 <= angle < 45:
#                                        horizontal = False
#                                else:
#                                        horizontal = True
                                ratio = size[0]/size[1]
                        elif i == 3:
#                                if 0 <= angle < 45:
#                                        horizontal = True
#                               else:
#                                        horizontal = False
                                ratio = size[1]/size[0]
                        delta = delta1
                        
#       print(horizontal,ratio)
                if area >= 20000:
#                       if horizontal == True and 0.35 <= ratio <= 1:
#                               quickTest = True
#                       elif horizontal == False and 0.35 <= ratio <= 1:
                        if 0.4 <= ratio <= 1:
                                test = True
                        else:
                                test = False
                return test


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

source = [0, 1]

capLeft  = cv2.VideoCapture(0)
capRight = cv2.VideoCapture(1)

count = 30;
case = 0; # 0 = calibrate, 1 undistort
print("Collecting data...")
print(count)
while(capLeft.isOpened() and capRight.isOpened()):
# Capture frame-by-frame
        ret, imageLeft  = capLeft.read()
        ret, imageRight = capRight.read()
        images = [imageLeft, imageRight]
        if case = 0
            while(count > 0):
                    for src in source
                        grey[src]  = cv2.cvtColor(imageLeft,cv2.COLOR_BGR2GRAY)

                        # Find the chess board corners
                        ret[src], corners[src]  = cv2.findChessboardCorners(grey[src], (9,6),None)

                        test[src] = [False, False]

                    # If found, add object points, image points (after refining them)
                    if ret[0] == True and ret[1] == True:
                        for src in source
                            corners2[src] = cv2.cornerSubPix(grey[src],corners[src],(11,11),(-1,-1),criteria)

                            # Draw and display the corners
                            image[src] = cv2.drawChessboardCorners(image[src], (9,6), corners2[src], ret[src])

                            rect[src]  = cv2.minAreaRect(cornersLeft2)
                            boxLeft  = cv2.boxPoints(rectLeft)
                            boxLeft2 = np.int0(boxLeft)


                            sizeLeft  = rectLeft[1]
                            sizeRight = rectLeft[1]
                            firstLeft  = cornersLeft2[0,0]
                            firstRight = cornersRight[0,0]

                            testLeft  = quickTest(boxLeft, sizeLeft, firstLeft, rectLeft)
                            testRight = quickTest(boxRight, sizeRight, firstRight, rectRight)

                            if testLeft == True and testRight == True:
                                    imagePointsLeft.append(cornersLeft2)
                                    imagePointsRight.append(cornersRight2)
                                    objectPoints.append(objp)
                                    cv2.drawContours(imageLeft,[boxLeft2],0,(0,255,0),2)
                                    cv2.drawContours(imageRight,[boxRight2],0,(0,255,0),2)
                                    count = count - 1
                                    print(count)
                            else:
                                    cv2.drawContours(imageLeft,[boxLeft2],0,(0,0,255),2)
                                    cv2.drawContours(imageRight,[boxRight2],0,(0,0,255),2)
                                    
                    imageCombined = np.concatenate((imageLeft, imageRight), axis=1)
                    cv2.imshow('img',imageCombined)

                    if cv2.waitKey(50) & 0xFF == ord('q'):
                            break
            print("Data collected...")
            print("Calibrating indiviual cameras...")
            #K1, D1, K2, D2, R, T, E, F = None
            imageSize = greyLeft.shape[::-1]
            print("Left...")
            rt, K1, D1, R1, T1 = cv2.calibrateCamera(objectPoints, imagePointsLeft, imageSize, None, None)
            print("Right...")
            rt, K2, D2, R2, T2 = cv2.calibrateCamera(objectPoints, imagePointsRight, imageSize, None, None)
            print("left", K1, D1)
            print("right", K2, D2)
            print("Calibrating stereo cameras...")
            stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 100, 1e-5)
            
            retVal, K1, D1, K2, D2, R, T, E, F = cv2.stereoCalibrate(objectPoints, imagePointsLeft, imagePointsRight, K1, D1, K2, D2, imageSize, criteria=stereocalib_criteria, flags=cv2.CALIB_FIX_INTRINSIC);
            print("left", K1, D1)
            print("right", K2, D2)
            print(R, T, E, F)

            alpha = 0
            flags = cv2.CALIB_ZERO_DISPARITY
            P1 = None
            P2 = None
            Q = None
            R1 = None
            R2 = None

            R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(K1, D1, K2, D2, imageSize, R, T, R1, R2, P1, P2, Q, flags, alpha)

            print(R1)
            print(R2)
            print(P1)
            print(P2)
            print(Q)

        if case = 1
            # undistort
        break
# When everything done, release the capture
capLeft.release()
capRight.release()
cv2.destroyAllWindows()

