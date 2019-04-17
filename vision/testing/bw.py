import numpy as np
import cv2
from datetime import datetime

def losslessResize(inputArray, outputSize):
    inputSize = inputArray.shape

    n = inputSize[1]/outputSize[1]
    m = inputSize[0]/outputSize[0]

    middleSize = (inputSize[0], outputSize[1])

    middleArray = np.empty(middleSize)
    values = []
    for i in range(0, middleSize[0]):
        for j in range(0, outputSize[1]):
            k = int(np.floor(n*j))
            while k < n*(j+1):
                values.append(inputArray[i,k])
                k = k+1
                middleArray[i,j] = max(values)
            values = []

    outputArray = np.empty(outputSize)

    values = []
    for j in range(0, outputSize[1]):
        for i in range(0, outputSize[0]):
            k = int(np.floor(m*i))
            while k < m*(i+1):
                values.append(middleArray[k,j])
                k = k+1
                outputArray[i,j] = max(values)
            values = []
    
    return np.uint8(outputArray)

# Set up cameras
capLeft  = cv2.VideoCapture(0)
capRight  = cv2.VideoCapture(1)

# Define the codec and create VideoWriter object
WIDTH = int(capLeft.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(capLeft.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(WIDTH,HEIGHT)

filename = str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.avi';

print('filename = '+filename)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
addFrame = cv2.VideoWriter(filename,fourcc, 20.0, (WIDTH*2,HEIGHT))

while(capLeft.isOpened() and capRight.isOpened()):
        # Capture frame-by-frame
        ret, imageLeft  = capLeft.read()
        ret, imageRight = capRight.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(imageLeft, cv2.COLOR_BGR2GRAY)
#        print(gray)

        gray1 = losslessResize(gray, (100, 100))
#        print(gray1)

        cv2.imshow('grey', gray)
        cv2.imshow('small', gray1)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
capLeft.release()
capRight.release()
cv2.destroyAllWindows()
