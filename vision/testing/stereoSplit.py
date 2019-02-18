import numpy as np
import cv2
from datetime import datetime

# Set up cameras
capCombined  = cv2.VideoCapture('output.avi')

# Define the codec and create VideoWriter object
WIDTH = int(capCombined.get(cv2.CAP_PROP_FRAME_WIDTH))/2
HEIGHT = int(capCombined.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(WIDTH,HEIGHT)

while(capCombined.isOpened()):
# Capture frame-by-frame
	ret, imageCombined  = capCombined.read()
	if ret == False:
		break
# Our operations on the frame come here
	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	imageLeft = imageCombined[0:HEIGHT, 0:WIDTH]
	imageRight = imageCombined[0:HEIGHT, WIDTH+1:2*WIDTH]
# Display the resulting frame
	cv2.imshow('left',imageLeft)
	cv2.imshow('right',imageRight)

	cv2.imshow('combined',imageCombined)

	if cv2.waitKey(100) & 0xFF == ord('q'):
		break

# When everything done, release the capture
capCombined.release()
cv2.destroyAllWindows()
