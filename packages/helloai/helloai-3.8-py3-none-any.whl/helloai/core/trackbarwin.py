import cv2
import numpy as np
import uuid
from .window import Window
from .image import Image

__all__ = ["TrackbarWindow"]


def nothing(x):
    pass


class TrackbarWindow(Window):
    def __init__(self, name):
        super().__init__(name)
        cv2.createTrackbar("Value", self.name, 0, 100, nothing)

    def get_value(self):
        val = cv2.getTrackbarPos("Value", self.name)
        return val

    def set_value(self, val):
        cv2.setTrackbarPos("Value", self.name, val)
