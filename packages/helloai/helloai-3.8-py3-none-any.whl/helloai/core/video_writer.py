import os
import cv2
import uuid
from helloai.core.image import Image

__all__ = ["VideoWriter"]


class VideoWriter:
    def __init__(self, path, options):
        self.__options = options

        self.__width = int(self.__options["width"])
        self.__height = int(self.__options["height"])
        self.__fps = self.__options["fps"]
        self.__output_path = path

        self.__fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 코덱 설정 (MP4 코덱)
        self.__writer = cv2.VideoWriter(self.__output_path, 
                                        self.__fourcc, 
                                        self.__fps, 
                                        (self.__width, self.__height))
        self.__frame_count = 0
        
    @property
    def frame_count(self):
        return self.__frame_count

    def write(self, img):
        if not isinstance(img, Image):
            return
        if self.__writer:
            self.__frame_count += 1
            frame = img.frame

            # 이미지의 크기가 비디오 설정 크기와 일치하지 않으면 크기 조정
            if (frame.shape[1], frame.shape[0]) != (self.__width, self.__height):
                frame = cv2.resize(frame, (self.__width, self.__height))
            self.__writer.write(img.frame)

    def release(self):
        if self.__writer is not None:
            self.__writer.release()
            self.__writer = None

    def __del__(self):
        if self.__writer is not None:
            self.__writer.release()

    def get_info(self):
        """
        비디오의 기본 정보를 반환합니다.
        Returns:
            dict: 비디오의 너비, 높이, FPS, 총 프레임 수
        """
        return {
            "width": self.__width,
            "height": self.__height,
            "fps": self.__fps,
            "frame_count": self.__frame_count
        }