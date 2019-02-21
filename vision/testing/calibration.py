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

capLeft  = cv2.VideoCapture(0)
capRight = cv2.VideoCapture(1)

count = 30;

print("Collecting data...")
print(count)
while(capLeft.isOpened() and capRight.isOpened()):
        while(count > 0):
                # Capture frame-by-frame
                ret, imageLeft  = capLeft.read()
                ret, imageRight = capRight.read()

                greyLeft  = cv2.cvtColor(imageLeft,cv2.COLOR_BGR2GRAY)
                greyRight = cv2.cvtColor(imageRight,cv2.COLOR_BGR2GRAY)
#               cv2.imshow('img',greyLeft)

                # Find the chess board corners
                retLeft,  cornersLeft  = cv2.findChessboardCorners(greyLeft, (9,6),None)
                retRight, cornersRight = cv2.findChessboardCorners(greyRight, (9,6),None)

                testLeft = False
                testRight = False

                # If found, add object points, image points (after refining them)
                if retLeft == True and retRight == True:
                        cornersLeft2 = cv2.cornerSubPix(greyLeft,cornersLeft,(11,11),(-1,-1),criteria)
                        cornersRight2 = cv2.cornerSubPix(greyRight,cornersRight,(11,11),(-1,-1),criteria)

                        # Draw and display the corners
                        imageLeft = cv2.drawChessboardCorners(imageLeft, (9,6), cornersLeft2, retLeft)
                        imageRight = cv2.drawChessboardCorners(imageRight, (9,6), cornersRight2, retRight)

                        rectLeft  = cv2.minAreaRect(cornersLeft2)
                        rectRight = cv2.minAreaRect(cornersRight2)
                        boxLeft  = cv2.boxPoints(rectLeft)
                        boxRight = cv2.boxPoints(rectRight)
                        boxLeft2 = np.int0(boxLeft)
                        boxRight2 = np.int0(boxRight)

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
        print("1")
        rt, K1, D1, R1, T1 = cv2.calibrateCamera(objectPoints, imagePointsLeft, imageSize, None, None)
        print("2")
        rt, K2, D2, R2, T2 = cv2.calibrateCamera(objectPoints, imagePointsRight, imageSize, None, None)
        print("left", K1, D1)
        print("right", K2, D2)
        print("Calibrating stereo cameras...")
        stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 100, 1e-5)
        
        retVal, K1, D1, K2, D2, R, T, E, F = cv2.stereoCalibrate(objectPoints, imagePointsLeft, imagePointsRight, K1, D1, K2, D2, imageSize, criteria=stereocalib_criteria, flags=cv2.CALIB_FIX_INTRINSIC);
        print("left", K1, D1)
        print("right", K2, D2)
        print(R, T, E, F)
        break
# When everything done, release the capture
capLeft.release()
capRight.release()
cv2.destroyAllWindows()

