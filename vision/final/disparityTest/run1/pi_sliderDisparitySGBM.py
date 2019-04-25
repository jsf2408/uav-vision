import cv2
import numpy as np
from timeit import default_timer as timer

##def nothing(x):
##    pass

##cv2.namedWindow('image')

imageCombined  = cv2.imread('480_2019-04-23-13-47-42.png')
calibration = np.load("480-10-calibration.npz")
imageSize = tuple(calibration["imageSize"])
xMapLeft = calibration["xMapLeft"]
yMapLeft = calibration["yMapLeft"]
xMapRight = calibration["xMapRight"]
yMapRight = calibration["yMapRight"]

### create trackbars for color change
##cv2.createTrackbar('1','image',0,10,nothing)
##cv2.createTrackbar('2','image',0,5,nothing)
##cv2.createTrackbar('3','image',5,20,nothing)
##cv2.createTrackbar('4','image',600,10000,nothing)
##cv2.createTrackbar('5','image',2400,10000,nothing)
##cv2.createTrackbar('6','image',20,255,nothing)
##cv2.createTrackbar('7','image',0,255,nothing)
##cv2.createTrackbar('8','image',1,255,nothing)
##cv2.createTrackbar('9','image',0,255,nothing)
##cv2.createTrackbar('10','image',0,255,nothing)
##cv2.createTrackbar('11','image',0,1,nothing)

WIDTH = imageCombined.shape[1]/2

imageLeft0 = imageCombined[:, 0:WIDTH]
imageRight0 = imageCombined[:, WIDTH:2*WIDTH]


##realLeft = cv2.remap(imageLeft, xMapLeft, yMapLeft, cv2.INTER_LINEAR)
##realRight = cv2.remap(imageRight, xMapRight, yMapRight, cv2.INTER_LINEAR)
##
##imageLeft = cv2.cvtColor(realLeft, cv2.COLOR_BGR2GRAY)
##imageRight = cv2.cvtColor(realRight, cv2.COLOR_BGR2GRAY)
##
##
##cv2.imshow('reall', realLeft)
##cv2.imshow('realr', realRight)

##while(1):
    # get current positions of four trackbars
    minDisparities = 0
    numDisparities = 32
    blockSize = 0
    p1 = 600
    p2 = 2400
    disp12MaxDiff = 20
    preFilterCap = 0
    uniquenessRatio = 0
    speckleWindowSize = 0
    speckleRange = 0
    doublePass = 0
##    if (blockSize % 2) == 0:
##        blockSize = blockSize +1
##    if (prefilterSize % 2) == 0:
##        prefilterSize = prefilterSize +1

    stereosgbm = cv2.StereoSGBM_create(minDisparities, numDisparities, \
                                       blockSize, p1, p2, disp12MaxDiff, \
                                       preFilterCap, uniquenessRatio, \
                                       speckleWindowSize, speckleWindowSize, \
                                       doublePass)
    time = 0
    for i in range(10):
        start = timer()
        realLeft = cv2.remap(imageLeft0, xMapLeft, yMapLeft, cv2.INTER_LINEAR)
        realRight = cv2.remap(imageRight0, xMapRight, yMapRight, cv2.INTER_LINEAR)

        imageLeft = cv2.cvtColor(realLeft, cv2.COLOR_BGR2GRAY)
        imageRight = cv2.cvtColor(realRight, cv2.COLOR_BGR2GRAY)
        
        disparityMap = stereosgbm.compute(imageLeft,imageRight)
        time = (timer() - start + time)/2
##    disparityMap = cv2.resize(disparityMap, (320, 240))
##    disparityMap = np.uint8(disparityMap)
##    
##    cv2.imshow('map',disparityMap)
    print(time)
##    k = cv2.waitKey(1) & 0xFF
##    if k == 27:
##        break
cv2.destroyAllWindows()
