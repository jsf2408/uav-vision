import numpy as np
import cv2
import os

def clickEvent(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
                global pointX,pointY,count,depthMap,pathData
                pointX = x
                pointY = y
                depthMapCross = cv2.line(depthMap,(x-5,y),(x+5,y),(0,255,0),1)
                depthMapCross = cv2.line(depthMap,(x,y-5),(x,y+5),(0,255,0),1)
                cv2.imshow('map', depthMapCross)
                
        if event == cv2.EVENT_LBUTTONUP and pointX != None:
                print(pointX, pointY)
                count = count + 1
                imageName = fileName0 + '--' + format(count, '05') + '.png'
                file.write(imageName + '\t' + str(pointX) + '\t' + str(pointY) + '\n')

                cv2.imwrite(os.path.join(pathData, imageName), depthMap)

                retMap, depthMap = capDepth.read()

pointX = None
pointY = None
count = 0

pathVideo = 'videos/stereoImage'
pathData = 'trainingData'
fileName0 = 'output'
fileName = fileName0 + '.avi'

textFile = 'trainingData.txt'
file = open(os.path.join(pathData, textFile),'a')
capDepth  = cv2.VideoCapture(os.path.join(pathVideo,fileName))

retMap, depthMap = capDepth.read()
cv2.namedWindow('map')
cv2.setMouseCallback('map', clickEvent)

while(retMap == True):
	cv2.imshow('map', depthMap)
	if cv2.waitKey(1) == 27:
		retMap, depthMap = capDepth.read()
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
capDepth.release()
cv2.destroyAllWindows()
