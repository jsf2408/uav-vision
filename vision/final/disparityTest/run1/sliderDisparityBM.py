import cv2
import numpy as np
from timeit import default_timer as timer

def nothing(x):
    pass

def clickEvent(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
                global pointX,pointY,count,disparityMap,pathData
                pointX = x
                pointY = y
                depth = disparityMap[y,x]
                print(depth)

cv2.namedWindow('image')
cv2.namedWindow('final')
cv2.setMouseCallback('final', clickEvent)

imageCombined  = cv2.imread('480_2019-04-23-13-47-42.png')
calibration = np.load("480-10-calibration.npz")
imageSize = tuple(calibration["imageSize"])
xMapLeft = calibration["xMapLeft"]
yMapLeft = calibration["yMapLeft"]
xMapRight = calibration["xMapRight"]
yMapRight = calibration["yMapRight"]
#focalLength = calibration["focalLength"]

# create trackbars for color change
cv2.createTrackbar('1','image',1,10,nothing)
cv2.createTrackbar('2','image',15,250,nothing)
cv2.createTrackbar('3','image',5,84,nothing)
cv2.createTrackbar('4','image',0,62,nothing)
cv2.createTrackbar('5','image',0,255,nothing)
cv2.createTrackbar('6','image',0,255,nothing)
cv2.createTrackbar('7','image',0,255,nothing)
cv2.createTrackbar('8','image',0,255,nothing)

WIDTH = imageCombined.shape[1]/2

HEIGHT = imageCombined.shape[0]

imageRight0 = imageCombined[:, 0:WIDTH]
imageLeft0 = imageCombined[:, WIDTH:2*WIDTH]



#cv2.imshow('im', imageLeft)


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

    time = 0
    for i in range(10):
        start = timer()
        stereobm = cv2.StereoBM_create(numDisparities,blockSize)
        stereobm.setPreFilterSize(prefilterSize)
        stereobm.setPreFilterType(cv2.STEREO_BM_PREFILTER_NORMALIZED_RESPONSE)
        stereobm.setPreFilterCap(prefilterCap)
        stereobm.setTextureThreshold(textureThreshold)
        stereobm.setSpeckleWindowSize(speckleWindowSize)
        stereobm.setSpeckleRange(speckleRange)
        stereobm.setUniquenessRatio(uniquenessRatio)

        realLeft = cv2.remap(imageLeft0, xMapLeft, yMapLeft, cv2.INTER_LINEAR)
        realRight = cv2.remap(imageRight0, xMapRight, yMapRight, cv2.INTER_LINEAR)

        realLeft = realLeft[:(HEIGHT-10), :]
        realRight = realRight[10:, :]

        imageLeft = cv2.cvtColor(realLeft, cv2.COLOR_BGR2GRAY)
        imageRight = cv2.cvtColor(realRight, cv2.COLOR_BGR2GRAY)
        disparityMap = stereobm.compute(imageLeft,imageRight)
        time = (timer() - start + time)/2
        
#    disparityMap = cv2.resize(disparityMap, (320, 240))
    disparityMap = np.uint8(disparityMap)
    print(time)
    cv2.imshow('final',cv2.resize(disparityMap, (640,480)))
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
