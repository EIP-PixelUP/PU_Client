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


class OpenCV_SuperRes(Upscaler):
    def __init__(self, filename, model_type, scale):
        print(f"Using model: {filename} type: {model_type} scale: {scale}")
        self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
        self.sr.readModel(f"models/{filename}")
        self.sr.setModel(model_type, int(scale))
        self.sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.scale = scale

    def upscale(self, frame, scale):
        if scale != self.scale:
            raise ScaleError(scale, [self.scale])
        return self.sr.upsample(frame)


class OpenCV_FSRCNN(OpenCV_SuperRes):
    def __init__(self, scale, small=True):
        small = "-small" if small else ""
        model_name = f"FSRCNN{small}_x{scale}.pb"
        super().__init__(model_name, "fsrcnn", scale)


class OpenCV_ESPCN(OpenCV_SuperRes):
    def __init__(self, scale):
        super().__init__(f"ESPCN_x{scale}.pb", "espcn", scale)


def opencv_scale(frame, ratio, *, interpolation=cv2.INTER_AREA):
    dim = (int(frame.shape[1] * ratio), int(frame.shape[0] * ratio))
    return cv2.resize(frame, dim, interpolation=interpolation)


class OpenCV_Interpolation(Upscaler):
    def upscale(self, frame, scale):
        return opencv_scale(frame, scale)
