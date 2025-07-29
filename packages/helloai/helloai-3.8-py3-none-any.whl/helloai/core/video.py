import os
import cv2
from helloai.core.image import Image

__all__ = ["Video"]


class Video:
    def __init__(self, name):
        self.__name = name
        self.__capture = cv2.VideoCapture(name)
        self.__width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.__height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__frame_count = int(self.__capture.get(cv2.CAP_PROP_FRAME_COUNT))  # 총프레임수
        self.__frame_rate = int(self.__capture.get(cv2.CAP_PROP_FPS))  # 프레임레이트(fps)
        self.__fps = self.__frame_rate
        self.__fcc = None
        self.__out = None
        self.__fps = self.__frame_rate
        self.__writable = False

    def get_recorder(self, path, name):
        if self.__out:
            return self
        # mp4
        self.__fcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
        self.__out = cv2.VideoWriter(
            os.path.join(path, f"{name}.mp4"),
            self.__fcc,
            self.__fps,
            (self.__width, self.__height),
        )
        print("recorder name :", os.path.join(path, f"{name}.mp4"))
        return self

    def read(self):
        if self.__capture.get(cv2.CAP_PROP_POS_FRAMES) == self.__capture.get(
            cv2.CAP_PROP_FRAME_COUNT
        ):
            print("영상 재상이 끝났습니다")
            return None

        ret, frame = self.__capture.read()
        if ret:
            return Image(frame)
        else:
            return None

    @property
    def is_end(self):
        return self.__capture.get(cv2.CAP_PROP_POS_FRAMES) == self.__capture.get(
            cv2.CAP_PROP_FRAME_COUNT
        )

    @property
    def options(self):
        return {"height": self.__height, "width": self.__width, "fps": self.__fps}

    @property
    def frame_count(self):
        return self.__frame_count

    def write(self, img):
        if not isinstance(img, Image):
            return
        if self.__out:
            self.__out.write(img.frame)

    def release(self):
        # body of destructor
        if self.__capture is not None:
            self.__capture.release()
            self.__capture = None

        if self.__out is not None:
            self.__out.release()
            self.__out = None

    def __del__(self):
        # body of destructor
        if self.__capture is not None:
            self.__capture.release()

        if self.__out is not None:
            self.__out.release()
