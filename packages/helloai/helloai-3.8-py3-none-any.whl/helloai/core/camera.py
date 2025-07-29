# Part of the MoyaLab project - http://moyalab.com
# Copyright (C) 2019 Moyalab (immoyalab@gmail.com)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import builtins
import cv2
import time
from helloai.core.image import Image
from helloai.core.image import ColorSpace
from helloai.core.config import *

__all__ = ["Camera"]

DEFAULT_SIZE = (builtins.WIDTH, builtins.HEIGHT)

# camera 640 x 480
# scratch3.0  w h -> 480 x 360


class Camera:
    def __init__(self, num=0, flip=1, crop=False, scale=1, fps=False, size=(640, 480)):
        """카메라 객체
        카메라는 입력을 기본적으로 반전시켜서 사용한다. (거울과 같은 효과)
        Args:
            num (int, optional): 카메라 식별 번호. Defaults to 0.
            flip (bool, optional): 화면을 반전시킨다. 0 반전 없슴. 1 좌우 반전, 2 상하 반전 Defaults to 0.
            crop (bool, optional): 폭과 높이를 일치시킨다. Defaults to False.
            scale (int, optional): 화면 키우기. Defaults to 1.
        """
        self.__num = num
        self.__scale = scale
        self.__flip = flip
        self.__crop = crop
        self.__fps = fps
        self.__frame = None
        self.__capture = cv2.VideoCapture(num, cv2.CAP_DSHOW)
        time.sleep(1)  # 1sec 카메라가 인식될때 시간이 조금 필요
        # self.__size = size
        self.__capture.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.__capture.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
        self.__capture.set(cv2.CAP_PROP_BUFFERSIZE, 0)

    def is_opened(self):
        if not self.__capture or not self.__capture.isOpened():
            return False
        return True

    def read(self):
        if not self.__capture.isOpened():
            print("카메라가 동작하지 않습니다")
            return None
        # fps계산위해서
        timer = cv2.getTickCount()
        ret, frame = self.__capture.read()
        # self.__fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)

        if ret:
            width = self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
            height = self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

            if self.__flip == 1:
                frame = cv2.flip(frame, 1)  # 1 좌우, 0 상하 반전
            elif self.__flip == 2:
                frame = cv2.flip(frame, 0)  # 1 좌우, 0 상하 반전

            if self.__crop:
                if width > height:
                    frame = self.__center_crop(frame, [height, height])
                else:
                    frame = self.__center_crop(frame, [width, width])

            h, w, c = frame.shape
            # frame = cv2.resize(frame, dsize=self.__size, interpolation=cv2.INTER_LINEAR)

            # if w > DEFAULT_SIZE or h > DEFAULT_SIZE:
            #     frame = self.__resize(frame)

            if self.__scale > 0:
                frame = cv2.resize(
                    frame,
                    dsize=(w * self.__scale, h * self.__scale),
                    interpolation=cv2.INTER_LINEAR,
                )
            if self.__fps:
                frame = self.__put_fps(frame)
            self.__frame = frame
            return Image(self.__frame, ColorSpace.BGR)
        else:
            return None

    def __center_crop(self, img, dim):
        """Returns center cropped image
        img: image to be center cropped
        dim: dimensions (width, height) to be cropped from center
        """
        width, height = img.shape[1], img.shape[0]
        # process crop width and height for max available dimension
        crop_width = dim[0] if dim[0] < img.shape[1] else img.shape[1]
        crop_height = dim[1] if dim[1] < img.shape[0] else img.shape[0]

        mid_x, mid_y = int(width / 2), int(height / 2)
        cw2, ch2 = int(crop_width / 2), int(crop_height / 2)
        crop_img = img[mid_y - ch2 : mid_y + ch2, mid_x - cw2 : mid_x + cw2]
        return crop_img

    def __resize(self, frame):
        h, w, c = frame.shape
        ratio = 1
        if h > w:
            ratio = DEFAULT_SIZE / h
        else:
            ratio = DEFAULT_SIZE / w

        frame = cv2.resize(
            frame, dsize=(0, 0), fx=ratio, fy=ratio, interpolation=cv2.INTER_LINEAR
        )
        return frame

    def __get_fps(self):
        return builtins.fps

    def __put_fps(self, frame):
        # cv2.putText(frame,"fps=",(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(127,127,255),2)
        # cv2.putText(frame,str(int(builtins.fps)),(75,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(127,127,255),2)
        fps_txt = "FPS %01.f" % builtins.fps
        cv2.putText(frame, fps_txt, (0, 18), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
        return frame

    def close(self):
        if self.__capture is not None:
            self.__capture.release()

    def __del__(self):
        # body of destructor
        if self.__capture is not None:
            self.__capture.release()
