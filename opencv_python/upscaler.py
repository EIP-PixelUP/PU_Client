#!/usr/bin/env python3

import cv2
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


class Upscaler(ABC):
    @abstractmethod
    def upscale(self, frame, scale: float):
        pass


@dataclass
class ScaleError:
    scale: float
    supported: List[float]

    def __str__(self):
        return f"This upscaler cannot upscale using scale {self.scale}." \
            + f" Available: {self.supported}"


class OpenCV_FSRCNN(Upscaler):
    def __init__(self):
        self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
        self.sr.readModel("../FSRCNN-small_x2.pb")
        self.sr.setModel("fsrcnn", 2)
        self.sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def upscale(self, frame, scale):
        if scale != 2:
            raise ScaleError(scale, [2.0])
        return self.sr.upsample(frame)


def opencv_scale(frame, ratio, *, interpolation=cv2.INTER_AREA):
    dim = (int(frame.shape[1] * ratio), int(frame.shape[0] * ratio))
    return cv2.resize(frame, dim, interpolation=interpolation)


class OpenCV_Interpolation(Upscaler):
    def upscale(self, frame, scale):
        return opencv_scale(frame, scale)
