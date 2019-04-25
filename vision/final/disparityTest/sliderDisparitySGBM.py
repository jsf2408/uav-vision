import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('image')

imageCombined  = cv2.imread('480_2019-04-23-13-47-42.png')
calibration = np.load("480-10-calibration.npz")
imageSize = tuple(calibration["imageSize"])
xMapLeft = calibration["xMapLeft"]
yMapLeft = calibration["yMapLeft"]
xMapRight = calibration["xMapRight"]
yMapRight = calibration["yMapRight"]

# create trackbars for color change
cv2.createTrackbar('1','image',0,10,nothing)
cv2.createTrackbar('2','image',0,5,nothing)
cv2.createTrackbar('3','image',5,250,nothing)
cv2.createTrackbar('4','image',600,10000,nothing)
cv2.createTrackbar('5','image',2400,10000,nothing)
cv2.createTrackbar('6','image',20,255,nothing)
cv2.createTrackbar('7','image',16,255,nothing)
cv2.createTrackbar('8','image',1,255,nothing)
cv2.createTrackbar('9','image',100,255,nothing)
cv2.createTrackbar('10','image',20,255,nothing)
cv2.createTrackbar('11','image',0,1,nothing)

WIDTH = imageCombined.shape[1]/2

imageLeft = imageCombined[:, 0:WIDTH]
imageRight = imageCombined[:, WIDTH:2*WIDTH]

realLeft = cv2.remap(imageLeft, xMapLeft, yMapLeft, cv2.INTER_LINEAR)
realRight = cv2.remap(imageRight, xMapRight, yMapRight, cv2.INTER_LINEAR)

imageLeft = cv2.cvtColor(realLeft, cv2.COLOR_BGR2GRAY)
imageRight = cv2.cvtColor(realRight, cv2.COLOR_BGR2GRAY)

cv2.imshow('reall', realLeft)
cv2.imshow('realr', realRight)

while(1):
    # get current positions of four trackbars
    minDisparities = cv2.getTrackbarPos('1','image')
    numDisparities = (cv2.getTrackbarPos('2','image')+1)*16
    blockSize = cv2.getTrackbarPos('3','image')
    p1 = cv2.getTrackbarPos('4','image')
    p2 = cv2.getTrackbarPos('5','image')
    disp12MaxDiff = cv2.getTrackbarPos('6','image')
    preFilterCap = cv2.getTrackbarPos('7','image')
    uniquenessRatio = cv2.getTrackbarPos('8','image')
    speckleWindowSize = cv2.getTrackbarPos('9','image')
    speckleRange = cv2.getTrackbarPos('10','image')
    doublePass = cv2.getTrackbarPos('11','image')
##    if (blockSize % 2) == 0:
##        blockSize = blockSize +1
##    if (prefilterSize % 2) == 0:
##        prefilterSize = prefilterSize +1

    stereosgbm = cv2.StereoSGBM_create(minDisparities, numDisparities, \
                                       blockSize, p1, p2, disp12MaxDiff, \
                                       preFilterCap, uniquenessRatio, \
                                       speckleWindowSize, speckleWindowSize, \
                                       doublePass)
    
    disparityMap = stereosgbm.compute(imageLeft,imageRight)
    disparityMap = cv2.resize(disparityMap, (320, 240))
    disparityMap = np.uint8(disparityMap)
    
    cv2.imshow('map',disparityMap)
    print(disparityMap[0,0])
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
