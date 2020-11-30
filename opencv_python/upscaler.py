#!/usr/bin/env python3
#
import cv2
import sys

cap = cv2.VideoCapture(sys.argv[1])

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.namedWindow("frame", cv2.WINDOW_FULLSCREEN)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
