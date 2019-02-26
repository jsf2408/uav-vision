import numpy as np
import cv2
#from matplotlib import pyplot as plt

calibration = np.load("testCalibration.npz")
imageSize = tuple(calibration["imageSize"])
xMapLeft = calibration["xMapLeft"]
yMapLeft = calibration["yMapLeft"]
xMapRight = calibration["xMapRight"]
yMapRight = calibration["yMapRight"]

# Set up cameras
capLeft  = cv2.VideoCapture(0)
capRight = cv2.VideoCapture(1)

while(capLeft.isOpened() and capRight.isOpened()):
    # Capture frame-by-frame
    ret, imageLeft  = capLeft.read()
    ret, imageRight = capRight.read()

    realLeft = cv2.remap(imageLeft, xMapLeft, yMapLeft, cv2.INTER_LINEAR)
    realRight = cv2.remap(imageRight, xMapRight, yMapRight, cv2.INTER_LINEAR)

    imageLeft = cv2.cvtColor(realLeft, cv2.COLOR_BGR2GRAY)
    imageRight = cv2.cvtColor(realRight, cv2.COLOR_BGR2GRAY)

    # Our operations on the frame com
    # When everything done, release the capture

    stereo = cv2.StereoBM_create(64,7)
    bm = stereo.compute(imageLeft,imageRight)
    bm = np.uint8(bm)

    stereo = cv2.StereoSGBM_create(0, 96, 5, 600, 2400, 20, 16, 1, 100, 20, True)
    sgbm = stereo.compute(imageLeft,imageRight)
    sgbm = np.uint8(sgbm)

    cv2.imshow('Left Image', imageLeft)
    cv2.imshow('BM Disparity Map', bm)
    cv2.imshow('SGBM Disparity Map', sgbm)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
