import numpy as np
import cv2
#from matplotlib import pyplot as plt

# Set up cameras
capLeft  = cv2.VideoCapture(0)
capRight = cv2.VideoCapture(1)


#while(capLeft.isOpened() and capRight.isOpened()):
# Capture frame-by-frame
ret, imageLeft  = capLeft.read()
ret, imageRight = capRight.read()

imageLeft = cv2.cvtColor(imageLeft, cv2.COLOR_BGR2GRAY)
imageRight = cv2.cvtColor(imageRight, cv2.COLOR_BGR2GRAY)

# Our operations on the frame com
# When everything done, release the capture

stereo = cv2.StereoBM_create(blockSize=15)
bm = stereo.compute(imageLeft,imageRight)
bm = np.uint8(bm)

stereo = cv2.StereoSGBM_create(0, 16, 15)
sgbm = stereo.compute(imageLeft,imageRight)
sgbm = np.uint8(sgbm)

cv2.imshow('Left Image', imageLeft)
cv2.imshow('BM Disparity Map', bm)
cv2.imshow('SGBM Disparity Map', sgbm)
cv2.waitKey()
cv2.destroyAllWindows()
