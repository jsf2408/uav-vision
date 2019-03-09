import numpy as np
import cv2
import os

x = None
y = None
count = 0

pathVideo = 'videos/stereoImage'
pathData = 'trainingData'
fileName0 = 'output'
fileName = fileName0 + '.avi'

capDepth  = cv2.VideoCapture(os.path.join(pathVideo))
retMap, depthMap = capDepth.read()

def clickEvent(event, x, y, flags, param, count):
        if event == cv2.EVENT_LBUTTONDOWN:
                print('1')
                print(x, y)
                count = count + 1
                imageName = fileName0 + '--' + format(count, '05') + '.png'

                print(imageName)

                cv2.imwrite(os.path.join(pathData, imageName), depthMap)

                retMap, depthMap = capDepth.read()

                

while(retMap == True):

# Display the resulting frame
	cv2.imshow('map', depthMap)

        print('1')
        print(x,y)
	cv2.setMouseCallback('map', clickEvent)
	print('2')
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
        print('3')
# When everything done, release the capture
capDepth.release()
cv2.destroyAllWindows()
