#!/usr/bin/env python3
#
import cv2
from cv2 import dnn_superres
import sys
import numpy as np

screen = (1920, 1080)
downscale_ratio = 2
sr = dnn_superres.DnnSuperResImpl_create()
sr.readModel("../FSRCNN-small_x2.pb")
sr.setModel("fsrcnn", 2)
sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


def scale(frame, ratio, *, interpolation=cv2.INTER_AREA):
	dim = (int(frame.shape[1] * ratio), int(frame.shape[0] * ratio))
	return cv2.resize(frame, dim, interpolation=interpolation)


if __name__ == "__main__":
	cap = cv2.VideoCapture(sys.argv[1])
	window_fit_scale = None

	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		# Fit the frame to half the window
		if not window_fit_scale:
			window_fit_scale = screen[0] / 2.0 / frame.shape[1]

		frame = scale(frame, window_fit_scale)

		# downscale then upscale
		downscaled = scale(frame, 1 / downscale_ratio)
		upscaled = sr.upsample(downscaled)
		# upscaled = scale(downscaled, downscale_ratio)

		# Merge images
		merged = np.concatenate((frame, upscaled), axis=1)

		# Display the resulting frame
		cv2.imshow("result", merged)
		# cv2.imshow("downscaled", downscaled)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
