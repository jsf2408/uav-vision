import numpy as np
import cv2
from datetime import datetime
import os

calibration = np.load("testCalibration.npz")
imageSize = tuple(calibration["imageSize"])
xMapLeft = calibration["xMapLeft"]
yMapLeft = calibration["yMapLeft"]
xMapRight = calibration["xMapRight"]
yMapRight = calibration["yMapRight"]

bmFile = 'bm.txt'
file = open(bmFile,'a')
# Define the codec and create VideoWriter object
WIDTH = 1280
HEIGHT = 720


# Capture frame-by-frame
imageCombined  = cv2.imread('2019-04-22-22-20-46.png')


imageLeft720 = imageCombined[0:HEIGHT, 0:WIDTH]
imageRight720 = imageCombined[0:HEIGHT, WIDTH:2*WIDTH]

imageLeft480 = cv2.resize(imageLeft720[:, 160:160+960], (640,480))
imageRight480 = cv2.resize(imageRight720[:, 160:160+960], (640,480))

imageLeft240 = cv2.resize(imageLeft480, (320, 240))
imageRight240 = cv2.resize(imageRight480, (320, 240))

left = [imageLeft720, imageLeft480, imageLeft240]
right = [imageRight720, imageRight480, imageRight240]
for i in range(len(left)):
    imageLeft = left[i]
    imageRight = right[i]

    realLeft = cv2.remap(imageLeft, xMapLeft, yMapLeft, cv2.INTER_LINEAR)
    realRight = cv2.remap(imageRight, xMapRight, yMapRight, cv2.INTER_LINEAR)

    imageLeft = cv2.cvtColor(realLeft, cv2.COLOR_BGR2GRAY)
    imageRight = cv2.cvtColor(realRight, cv2.COLOR_BGR2GRAY)
    print(imageLeft.shape)
    print(imageRight.shape)

    numDisparities = np.arange(0, 100, 8)
    blockSize = np.arange(5, 9, 2)
    prefilterSize = np.arange(5,50,10)
    prefilterCap = np.arange(1,63,5)
    textureThreshold = np.arange(0, 20, 2)
    speckleWindowSize = np.arange(5, 50, 10)
    speckleRange = np.arange(0, 100, 10)
    uniquenessRatio = np.arange(5, 10, 2)
    count = 0
    for j in numDisparities:
        for k in blockSize:
            for l in prefilterSize:
                for m in prefilterCap:
                    for n in textureThreshold:
                        for o in speckleWindowSize:
                            for p in speckleRange:
                                for q in uniquenessRatio:
                                    count = count + 1
                                    print(count)
                                    stereobm = cv2.StereoBM_create(j,k)
                                    stereobm.setPreFilterSize(l)
                                    stereobm.setPreFilterType(cv2.STEREO_BM_PREFILTER_NORMALIZED_RESPONSE)
                                    stereobm.setPreFilterCap(m)
                                    stereobm.setTextureThreshold(n)
                                    stereobm.setSpeckleWindowSize(o)
                                    stereobm.setSpeckleRange(p)
                                    stereobm.setUniquenessRatio(q)

                                    disparityMap = stereobm.compute(imageLeft,imageRight)
                                    disparityMap = np.uint8(disparityMap)

                                    cv2.imshow('Left Image', imageLeft)
                                    cv2.imshow('Disparity Map', disparityMap)

                                    cv2.waitKey(1)

                                    blockTest = 1#input("Block?")
                                    poleTest = 1#input("Pole?")
                                    file.write(str(imageLeft.shape) + '\t' + str(j) + '\t' + str(k) + '\t' + str(l) + '\t' + str(m) +'\t' + str(o) + '\t' + str(p) +'\t' + str(q) +'\n')

    stereosgbm = cv2.StereoSGBM_create(0, 96, 5, 600, 2400, 20, 16, 1, 100, 20, True)
    sgbm = stereosgbm.compute(imageLeft,imageRight)
    sgbm = np.uint8(sgbm)

cv2.imshow('Left Image', imageLeft)
cv2.imshow('Disparity Map', disparityMap)      


while cv2.waitKey(100) & 0xFF != ord('q'):
        break

cv2.destroyAllWindows()
