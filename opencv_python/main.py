#!/usr/bin/env python3
#
import cv2
import sys
import numpy as np
from time import time

import upscaler

screen = (1920, 1080)
downscale_ratio = 2


def scale(frame, ratio, *, interpolation=cv2.INTER_AREA):
    dim = (int(frame.shape[1] * ratio), int(frame.shape[0] * ratio))
    return cv2.resize(frame, dim, interpolation=interpolation)


def get_fps(timestamps):
    timestamps.append(time())
    last_times = timestamps[-10:]
    return len(last_times) / (last_times[-1] - last_times[0])


if __name__ == "__main__":
    cap = cv2.VideoCapture(sys.argv[1])
    window_fit_scale = None
    upscaler = upscaler.OpenCV_FSRCNN()
    timestamps = [time()]

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Fit the frame to half the window
        if not window_fit_scale:
            print(frame.shape)
            window_fit_scale = screen[0] / 2.0 / frame.shape[1]
            print(window_fit_scale)

        frame = scale(frame, window_fit_scale)

        # downscale then upscale
        downscaled = scale(frame, 1 / downscale_ratio)
        upscaled = upscaler.upscale(downscaled, downscale_ratio)

        # Merge images
        merged = np.concatenate((frame, upscaled), axis=1)

        # Display FPS
        fps = get_fps(timestamps)
        cv2.putText(merged, f"FPS: {fps:.2f}", (50, 50),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        # Display the resulting frame
        cv2.imshow("result", merged)
        # cv2.imshow("downscaled", downscaled)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()