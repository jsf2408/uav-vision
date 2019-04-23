import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('image')

imageCombined  = cv2.imread('720_2019-04-23-14-05-17.png')
calibration = np.load("720-30-calibration.npz")
imageSize = tuple(calibration["imageSize"])
xMapLeft = calibration["xMapLeft"]
yMapLeft = calibration["yMapLeft"]
xMapRight = calibration["xMapRight"]
yMapRight = calibration["yMapRight"]

# create trackbars for color change
cv2.createTrackbar('1','image',0,10,nothing)
cv2.createTrackbar('2','image',0,250,nothing)
cv2.createTrackbar('3','image',0,250,nothing)
cv2.createTrackbar('4','image',0,62,nothing)
cv2.createTrackbar('5','image',0,255,nothing)
cv2.createTrackbar('6','image',0,255,nothing)
cv2.createTrackbar('7','image',0,255,nothing)
cv2.createTrackbar('8','image',0,255,nothing)

WIDTH = imageCombined.shape[1]/2

imageLeft = imageCombined[:, 0:WIDTH]
imageRight = imageCombined[:, WIDTH:2*WIDTH]

realLeft = cv2.remap(imageLeft, xMapLeft, yMapLeft, cv2.INTER_LINEAR)
realRight = cv2.remap(imageRight, xMapRight, yMapRight, cv2.INTER_LINEAR)

imageLeft = cv2.cvtColor(realLeft, cv2.COLOR_BGR2GRAY)
imageRight = cv2.cvtColor(realRight, cv2.COLOR_BGR2GRAY)

while(1):
    # get current positions of four trackbars
    numDisparities = cv2.getTrackbarPos('1','image') * 16
    blockSize = cv2.getTrackbarPos('2','image') + 5
    prefilterSize = cv2.getTrackbarPos('3','image') + 5
    prefilterCap = cv2.getTrackbarPos('4','image') + 1
    textureThreshold = cv2.getTrackbarPos('5','image')
    speckleWindowSize = cv2.getTrackbarPos('6','image')
    speckleRange = cv2.getTrackbarPos('7','image')
    uniquenessRatio = cv2.getTrackbarPos('8','image')

    if (blockSize % 2) == 0:
        blockSize = blockSize +1
    if (prefilterSize % 2) == 0:
        prefilterSize = prefilterSize +1

    stereobm = cv2.StereoBM_create(numDisparities,blockSize)
    stereobm.setPreFilterSize(prefilterSize)
    stereobm.setPreFilterType(cv2.STEREO_BM_PREFILTER_NORMALIZED_RESPONSE)
    stereobm.setPreFilterCap(prefilterCap)
    stereobm.setTextureThreshold(textureThreshold)
    stereobm.setSpeckleWindowSize(speckleWindowSize)
    stereobm.setSpeckleRange(speckleRange)
    stereobm.setUniquenessRatio(uniquenessRatio)
    
    disparityMap = stereobm.compute(imageLeft,imageRight)
    disparityMap = cv2.resize(disparityMap, (320, 240))
    disparityMap = np.uint8(disparityMap)
    
    cv2.imshow('image',disparityMap)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
