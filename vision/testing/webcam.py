import numpy as np
import cv2

capLeft  = cv2.VideoCapture(2)
capRight = cv2.VideoCapture(1)

while(capLeft.isOpened() and capRight.isOpened()):
# Capture frame-by-frame
	ret, imageLeft  = capLeft.read()
	ret, imageRight = capRight.read()

# Our operations on the frame come here
	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# Display the resulting frame
	cv2.imshow('left',imageLeft)
	cv2.imshow('right',imageRight)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
capLeft.release()
capRight.release()
cv2.destroyAllWindows()
