import numpy as np
import cv2
import glob
from math import sqrt

def quickTest(box, size, first, rect):
        delta = 100000
        area  = size[0]*size[1]
        horizontal = None
        angle = abs(rect[2])
##        print(box)
        for i in range(0,4):
                point = box[i]
                x1 = abs(first[0] - point[0])
                y1 = abs(first[1] - point[1])
                delta1 = sqrt(x1*x1+y1*y1)
##                print(i)
                test=False
                if delta1 < delta:
                        if i == 0:
##                                if 0 <= angle < 45:
##                                    horizontal = False
##                                    ratio = size[1]/size[0]
##                                else:
##                                    horizontal = True
                            ratio = size[0]/size[1]
                        elif i == 1:
##                               if 0 <= angle < 45:
##                                       horizontal = True
##                               else:
##                                       horizontal = False
                               ratio = size[1]/size[0]
                        elif i == 2:
##                               if 0 <= angle < 45:
##                                        horizontal = False
##                               else:
##                                        horizontal = True
                               ratio = size[0]/size[1]
                        elif i == 3:
##                               if 0 <= angle < 45:
##                                        horizontal = True
##                               else:
##                                        horizontal = False
                               ratio = size[1]/size[0]
                        delta = delta1
                        #print(i,horizontal)
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

cellSize = 27

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)*cellSize

# Arrays to store object points and image points from all the images.
objectPoints = [] # 3d point in real world space
imagePointsLeft = [] # 2d points in image plane.
imagePointsRight = []

capLeft  = cv2.VideoCapture(0)
capRight = cv2.VideoCapture(1)

count = 50

case = 0

print("Collecting data...")
print(count)
while(capLeft.isOpened() and capRight.isOpened()):
        # Capture frame-by-frame
        if case == 0:
                while(count > 0):
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

                        if cv2.waitKey(200) & 0xFF == ord('q'):
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

#                xMapLeft, yMapLeft = cv2.initUndistortRectifyMap(leftCameraMatrix, leftDistortionCoefficients, leftRectification, leftProjection, imageSize, cv2.CV_32FC1)
                xMapLeft, yMapLeft = cv2.initUndistortRectifyMap(K1, D1, R1, P1, imageSize, cv2.CV_32FC1)
                xMapRight, yMapRight = cv2.initUndistortRectifyMap(K2, D2, R2, P2, imageSize, cv2.CV_32FC1)

                print("Saving calibration...")
                np.savez_compressed("testCalibration", imageSize=imageSize, xMapLeft=xMapLeft, yMapLeft=yMapLeft, xMapRight=xMapRight, yMapRight=yMapRight)
                print("Saved.")
                
                case = 1
                
        if case == 1:
                ret, imageLeft  = capLeft.read()
                ret, imageRight = capRight.read()


##                cornersRight(:,:) = cornersRight(:,:)+640
##
##                print(cornersRight)
                
                realLeft = cv2.remap(imageLeft, xMapLeft, yMapLeft, cv2.INTER_LINEAR)
                realRight = cv2.remap(imageRight, xMapRight, yMapRight, cv2.INTER_LINEAR)

                greyLeft  = cv2.cvtColor(imageLeft,cv2.COLOR_BGR2GRAY)
                greyRight = cv2.cvtColor(imageRight,cv2.COLOR_BGR2GRAY)

                retLeft,  cornersLeft  = cv2.findChessboardCorners(greyLeft, (9,6),None)
                retRight, cornersRight = cv2.findChessboardCorners(greyRight, (9,6),None)

                if retRight == True:
                    cornersRight[:,:,1] = cornersRight[:,:,1] + 640
                
                imageCombinedTop = np.concatenate((imageLeft, imageRight), axis=1)
                imageCombinedBottom = np.concatenate((realLeft, realRight), axis=1)

                if retRight == True and retLeft == True:
                    size = np.shape(cornersLeft)
                    for i in range(size[0]):
                        cv2.line(imageCombinedBottom, tuple(cornersLeft[i,0,:]), tuple(cornersRight[i,0,:]), (0,0,255), thickness=5)
                
                imageCombined = np.concatenate((imageCombinedTop, imageCombinedBottom), axis=0)

                cv2.imshow('img',imageCombined)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
# When everything done, release the capture
capLeft.release()
capRight.release()
cv2.destroyAllWindows()

