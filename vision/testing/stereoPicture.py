import numpy as np
import cv2
from datetime import datetime

# Set up cameras
capLeft  = cv2.VideoCapture(0)
capRight = cv2.VideoCapture(1)

# Define the codec and create VideoWriter object
capLeft.set(3,1280)
capLeft.set(4,720)
capRight.set(3,1280)
capRight.set(4,720)

WIDTH = int(capLeft.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(capLeft.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(WIDTH,HEIGHT)

filename = str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))+'.png';

print('filename = '+filename)

while(capLeft.isOpened() and capRight.isOpened()):
# Capture frame-by-frame
	ret, imageLeft  = capLeft.read()
	ret, imageRight = capRight.read()

# Our operations on the frame come here
	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	imageCombined = np.concatenate((imageLeft, imageRight), axis=1)
# Display the resulting frame
#	cv2.imshow('left',imageLeft)
#	cv2.imshow('right',imageRight)
#	addFrame.write(imageCombined)
        

	cv2.imshow('combined',imageCombined)

	if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(filename, imageCombined)
	    break

# When everything done, release the capture
capLeft.release()
capRight.release()
cv2.destroyAllWindows()
