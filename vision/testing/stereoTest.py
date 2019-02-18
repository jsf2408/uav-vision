import numpy as np
import cv2

# Set up cameras
capLeft  = cv2.VideoCapture(0)
capRight = cv2.VideoCapture(1)

# Define the codec and create VideoWriter object
WIDTH = int(capLeft.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(capLeft.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(WIDTH,HEIGHT)

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

	cv2.imshow('combined',imageCombined)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
capLeft.release()
capRight.release()
cv2.destroyAllWindows()
