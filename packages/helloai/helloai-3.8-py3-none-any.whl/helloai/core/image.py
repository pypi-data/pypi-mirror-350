import builtins
import os
import re
import time
from PIL import Image as PImage
from PIL import ImageDraw
from PIL import ImageFont
from glob import glob
import matplotlib.image as img
import matplotlib.pyplot as plt
import cv2
# import imutils
import urllib.request
import scipy.spatial.distance as spsd
import numpy as np
import uuid

from helloai.core.config import *
from helloai.core.colors import Color
import  helloai.core.api as api


__all__ = ["Image", "ColorSpace", "ImageSet"]

FONT_PATH = "./assets/fonts/gulim.ttc"


class ColorSpace:
    UNKNOWN = "unknown"
    BGR = "bgr"
    GRAY = "gray"
    RGB = "rgb"
    HLS = "hls"
    HSV = "hsv"
    XYZ = "xyz"
    YCrCb = "ycrcb"
    BGRA = "bgra"
    RGBA = "rgba"


class Image:
    def __init__(self, frame=None, color_space=ColorSpace.BGR):
        if isinstance(frame, np.ndarray):
            self.__filename = None
            self.__frame = frame
            self.__image = self.__frame
            self.__array = self.__frame
            # shape (h, w, c)
            self.__height = self.__frame.shape[0]
            self.__width = self.__frame.shape[1]
            self.__colorSpace = color_space
            if len(self.__frame.shape) == 3:
                h, w, c = self.__frame.shape
                if c == 4:
                    self.__colorSpace = ColorSpace.BGRA
            else:
                self.__colorSpace = ColorSpace.GRAY
        else:
            raise Exception("파라메터의 형이 맞지않습니다")

    @property
    def width(self):
        if self.image is not None:
            return self.__frame.shape[1]
        return -1

    @property
    def height(self):
        if self.__frame is not None:
            return self.__frame.shape[0]
        return -1

    @property
    def center(self):
        """이미지의 중심 좌료

        Returns:
            turple: 좌표 (x, y)
        """
        return (self.__width // 2, self.__height // 2)

    @property
    def image(self):
        return self.__frame

    @property
    def frame(self):
        return self.__frame

    @property
    def frame_(self):
        return self.__frame
    
    @property
    def list(self):
        return self.frame

    @property
    def array(self):
        return np.array(self.__frame)

    def to_array(self):
        return np.array(self.__frame)

    @property
    def nparray(self):
        return np.array(self.__frame)

    def to_nparray(self):
        return np.array(self.__frame)

    # setter보다 먼저 같은 이름의 getter정의가 필요
    # 이 setter가 없으면 읽기 전용이 된다.
    # @name.setter
    # def name(self, frame):
    #     self.__frame = name

    @property
    def shape(self):
        """
        (height, weight, channel)
        """
        return self.__frame.shape

    @property
    def dimension(self):
        """
        차원수
        """
        return self.__frame.ndim

    @property
    def size_(self):
        """
        (width, height)
        """
        if self.__frame is not None:
            return (self.__frame.shape[1], self.__frame.shape[0])

    @property
    def colorspace(self):
        return self.__colorSpace

    @property
    def pixels(self):
        if self.__frame is not None:
            # return self.__frame.tolist()
            return self.__frame.tolist()
        return np.array([])

    @property
    def filename(self):
        return self.__filename

    def _rgba_to_bgra(color):
        if len(color) == 4:
            r, g, b, a = color
            return (b, g, r, a)
        elif len(color) == 3:
            # If the input is RGB, assume full opacity
            r, g, b = color
            return (b, g, r, 255)
        else:
            raise ValueError("Input color must be in RGBA or RGB format.")


    def fill_color(self, color=(0, 0, 0)):
        """
            이미지 전체를 설정 색상으로 입힘        
        """
        img =  api.new_image(color)
        self.__frame = img.frame
        return img

    def copy(self):
        return Image(np.copy(self.__frame), self.__colorSpace)

    def set_filename(self, name):
        self.__filename = name
        return self
    

    def __get_colorspace(self, frame):
        shape = frame.shape
        if len(shape) == 2:
            return ColorSpace.GRAY
        else:
            _, _, ch = shape
            if ch == 1:
                return ColorSpace.GRAY
            elif ch == 2:
                return ColorSpace.GRAY
            elif ch == 3:
                return ColorSpace.BGR
            elif ch == 4:
                return ColorSpace.BGRA
            else:
                return ColorSpace.GRAY

    # def __resize_with_border(self, size):
    #     frame = np.copy(self.__frame)
    #     old_size = frame.shape[:2]  # old_size is in (height, width) format

    #     ratio = float(size) / max(old_size)
    #     new_size = tuple([int(x * ratio) for x in old_size])

    #     # new_size should be in (width, height) format
    #     frame = cv2.resize(frame, (new_size[1], new_size[0]))
    #     delta_w = size - new_size[1]
    #     delta_h = size - new_size[0]

    #     top, bottom = 0 + delta_h // 2, delta_h - (delta_h // 2)
    #     left, right = 0 + delta_w // 2, delta_w - (delta_w // 2)

    #     #   부족한 부분 검은색으로 채워서 복사한다. https://can-do.tistory.com/4
    #     frame = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    #     return Image(frame), ratio, top, left

    def resize(self, width=0, height=0):
        """넓이와 높이를 지정해서 사이즈를 바꾼다.
        크기를 지정하지 않으면, 현재 이미지의 사이즈를 사용한다.

        Args:
            width (int, optional): 넓이. Defaults to 0. max : 1920
            height (int, optional): 높이. Defaults to 0. max: 1920

        Returns:
            [type]: [description]
        """
        
        
        if self.__frame is None:
            return Image(np.copy(self.__frame), self.__colorSpace)

        frame = np.copy(self.__frame)
        

        if width > 0 and height == 0:
            # 가로의 크기에 맞춰서, 비율을 유지하면서 리사이즈
            # resized = imutils.resize(frame, width=width)
            resized = cv2.resize(frame, (width, int(frame.shape[0] * (width / frame.shape[1]))))
            return Image(resized, self.__colorSpace)
        elif width <= 0 or height <= 0:
            # 크기를 지정하지 않으면, 현재 이미지의 크기를 그대로 사용한다.
            width = self.width if width == 0 else width
            height = self.height if height == 0 else height
            frame = cv2.resize(
                frame, dsize=(width, height), interpolation=cv2.INTER_LINEAR
            )
            return Image(frame, self.__colorSpace)
        elif width > MAX_DIMENSION or height > MAX_DIMENSION:
            return Image(frame, self.__colorSpace)
        else:
            
            frame = cv2.resize(
                self.__frame, dsize=(width, height), interpolation=cv2.INTER_LINEAR
            )
            return Image(frame, self.__colorSpace)

    def scale(self, scale=1):
        """넓이, 높이의 비율을 고정하고, 크기를 조절한다.

        Args:
            scale (int, optional): 크기 비율. Defaults to 1.

        Returns:
            Image: 크기 조절된 이미지
        """
        if self.__frame is None:
            return Image(np.copy(self.__frame), self.__colorSpace)
        frame = np.copy(self.__frame)
        h, w = frame.shape[0], frame.shape[1]

        # frame = cv2.resize(self.__frame, dsize=(w*scale, h*scale), interpolation=cv2.INTER_LINEAR)
        frame = cv2.resize(
            self.__frame,
            dsize=(0, 0),
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_LINEAR,
        )
        return Image(frame, self.__colorSpace)

    def adaptive_scale(self, size=None, color=(0, 0, 0)):
        """리사이즈해서 정사각형 이미지로 만든다. 부족한 부분은 검은색으로 채운다.

        Args:
            size (int): 이미지의 한 변 길이
            color (tuple): 여백부분의 색상 (r, g, b)

        Returns:
            Image: 리사이즈된 이미지
        """
        frame = np.copy(self.__frame)
        old_size = frame.shape[:2]  # old_size is in (height, width) format
        if not size:
            size = max(old_size)

        ratio = float(size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])

        # new_size should be in (width, height) format
        frame = cv2.resize(frame, (new_size[1], new_size[0]))
        delta_w = size - new_size[1]
        delta_h = size - new_size[0]

        top, bottom = 0 + delta_h // 2, delta_h - (delta_h // 2)
        left, right = 0 + delta_w // 2, delta_w - (delta_w // 2)

        color = color[::-1]
        #   부족한 부분 검은색으로 채워서 복사한다. https://can-do.tistory.com/4
        frame = cv2.copyMakeBorder(
            frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
        )
        # frame = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        return Image(frame), ratio, top, left

    # def squarize(self, crop=False, color=(0, 0, 0)):
    #     """넓이와 높이의 길이가 같도록 정사각형으로 만든다.

    #     Args:
    #         crop (bool, optional): 정사각형으로 자를것인지 (True), 이미지 전체를 정사각형으로 남기로 나머지 부분은 주어진 색상으로 채운다(False).
    #         color (tuple, optional): 나머지 영역을 채우는 색상 (r, g, b)
    #     """
    #     frame = np.copy(self.__frame)
    #     old_size = frame.shape[:2]  # old_size is in (height, width) format

    #     if crop:
    #         # center crop
    #         img_size = min(self.__frame.shape[:2])
    #         img = self.__center_crop((img_size, img_size))

    #         delta_w = old_size[1] - img_size
    #         delta_h = old_size[0] - img_size
    #         top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    #         left, right = delta_w // 2, delta_w - (delta_w // 2)
    #         return img, top, left
    #     else:
    #         # 테두리를 만들어서 정사각형화
    #         size = max(self.__frame.shape[:2])
    #         img, ratio, top, left = self.adaptive_scale(size, color)
    #         return img, top, left

    def squarize(self, size, crop=False, color=(0, 0, 0)):
        """넓이와 높이의 길이가 같도록 정사각형으로 만든다.

        Args:
            crop (bool, optional): 정사각형으로 자를것인지 (True), 이미지 전체를 정사각형으로 남기로 나머지 부분은 주어진 색상으로 채운다(False).
            color (tuple, optional): 나머지 영역을 채우는 색상 (r, g, b)
        """
        if crop:
            # center crop
            frame = np.copy(self.__frame)
            old_size = frame.shape[:2]  # old_size is in (height, width) format
            # 334, 500
            ratio = float(size) / min(old_size)

            new_size = tuple([int(x * ratio) for x in old_size])


            # 사이즈를 줄이고
            frame = cv2.resize(frame, (new_size[1], new_size[0]))

            # Crop하고
            img_size = min(new_size)


            img = self.__center_crop(frame, (img_size, img_size))


            # img = Image(frame)
            delta_w = new_size[1] - img_size
            delta_h = new_size[0] - img_size
            

            top, bottom = delta_h // 2, delta_h - (delta_h // 2)
            left, right = delta_w // 2, delta_w - (delta_w // 2)
            # 크롭의 경우는 랜드마크를 빼준다.
            # landmarks = ((landmarks * ratio)  - np.array([left, top])).astype(np.int)
            return img, ratio, top, left
        else:
            # 테두리를 만들어서 정사각형화
            # size = max(self.__frame.shape[:2])
            img, ratio, top, left = self.adaptive_scale(size, color)
            # 크롭의 경우는 랜드마크를 더한다.
            # landmarks = ((landmarks * ratio) + np.array([left, top])).astype(np.int)
            return img, ratio, top, left

    def ___resize(self, width=0, height=0, fx=0, fy=0):
        if self.__frame is None:
            return Image(np.copy(self.__frame), self.__colorSpace)

        frame = np.copy(self.__frame)
        if width <= 0 or height <= 0:
            if fx == 0 or fy == 0:
                return Image(np.copy(self.__frame), self.__colorSpace)
            else:
                frame = cv2.resize(
                    frame, dsize=(0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR
                )
                return Image(frame, self.__colorSpace)

        elif width > MAX_DIMENSION or height > MAX_DIMENSION:
            return Image(np.copy(self.__frame), self.__colorSpace)
        else:
            frame = cv2.resize(
                self.__frame, dsize=(width, height), interpolation=cv2.INTER_LINEAR
            )
            return Image(frame, self.__colorSpace)

    def crop(self, x=0, y=0, width=0, height=0, centered=False):
        """지정한 좌표를 시작점으로 해서 주어진 크기로 이미지를 자른다.

        Args:
            x (int, optional): 시작점 x 좌표. Defaults to 0.
            y (int, optional): 시작점 y 좌표. Defaults to 0.
            height (int, optional): 넓이. Defaults to 0.
            height (int, optional): 높아. Defaults to 0.
            centered (bool, optional): 이미지의 중심을 기준으로 자를것인가. Defaults to False.

        Returns:
            Image: 결과 이미지
        """
        # 0을 지정하면 현재 이미지의 크기를 사용한다.
        w = self.width if width == 0 else width
        h = self.height if height == 0 else height

        if centered:
            return self.__center_crop(self.__frame.copy(), (w, h))
        else:
            frame = self.__frame[y : y + h, x : x + w]
            return Image(np.copy(frame), self.__colorSpace)

    def __center_crop(self, frame, dim):
        # frame = np.copy(self.__frame)
        height, width = frame.shape[:2]  # old_size is in (height, width) format

        # crop_width = dim[0] if dim[0]<img.shape[1] else img.shape[1]
        # crop_height = dim[1] if dim[1]<img.shape[0] else img.shape[0]
        crop_width, crop_height = min(dim), min(dim)

        mid_x, mid_y = int(width / 2), int(height / 2)
        cw2, ch2 = int(crop_width / 2), int(crop_height / 2)
        crop_img = frame[mid_y - ch2 : mid_y + ch2, mid_x - cw2 : mid_x + cw2]

        return Image(crop_img)

    # ref : https://qiita.com/mo256man/items/82da5138eeacc420499d
    def __frame_to_pil(self, frame, colorspace):
        """
        frame에서 PIL이미지로 변환
        """
        frame = frame.copy()
        if colorspace == ColorSpace.BGR:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif colorspace == ColorSpace.GRAY:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif colorspace == ColorSpace.RGB:
            pass
        elif colorspace == ColorSpace.RGBA:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        elif colorspace == ColorSpace.BGRA:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = PImage.fromarray(frame)
        return im_pil

    def __pil_to_frame(self, im_pil, colorspace=ColorSpace.BGR):
        """
        PIL이미지에서 frame으로 변환
        """
        frame = np.asarray(im_pil)
        if colorspace == ColorSpace.BGR:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        elif colorspace == ColorSpace.GRAY:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        elif colorspace == ColorSpace.RGB:
            pass
        elif colorspace == ColorSpace.RGBA:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
        elif colorspace == ColorSpace.BGRA:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGRA)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame

    def overlay(self, img):
        pass
    

    def __rotate(self, frame, degree):
        """
        Rotate an image by a specified degree around its center.

        Parameters:
        - frame: The image to rotate (numpy array).
        - degree: The rotation angle in degrees.

        Returns:
        - Rotated image (numpy array).
        """
        # Calculate the center of the image
        (h, w) = frame.shape[:2]
        center = (w // 2, h // 2)

        # Generate the rotation matrix
        M = cv2.getRotationMatrix2D(center, degree, 1.0)

        # Perform the rotation
        rotated_frame = cv2.warpAffine(frame, M, (w, h))
        
        return rotated_frame

    def __rotate_bound(self, frame, degree):
        # 이미지 크기와 중심점 계산
        (h, w) = frame.shape[:2]
        center = (w // 2, h // 2)

        # 회전 행렬 생성
        M = cv2.getRotationMatrix2D(center, degree, 1.0)

        # 회전 후 새 이미지의 크기를 계산
        cos = abs(M[0, 0])
        sin = abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        # 회전 중심을 새로운 크기에 맞추어 조정
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]

        # 회전 적용
        rotated_frame = cv2.warpAffine(frame, M, (new_w, new_h))

        return rotated_frame

    def rotate(self, degree, resize=False):
        frame = np.copy(self.__frame)

        if resize:
            # frame = imutils.rotate(frame, degree)
            frame = self.__rotate(frame, degree)
        else:
            # frame = imutils.rotate_bound(frame, degree)
            frame = self.__rotate_bound(frame, degree)
        return Image(frame)

    def flip(self, mode="h"):
        """
        'h' : 좌우
        'v' : 상하
        'hv' : 상하좌우
        """
        frame = np.copy(self.__frame)
        if mode == "v":
            frame = cv2.flip(frame, 0)
        elif mode == "h":
            frame = cv2.flip(frame, 1)
        else:
            frame = cv2.flip(frame, -1)
        return Image(frame)

    def save(self, filename):
        pimg = self.__frame_to_pil(self.__frame.copy(), self.__get_colorspace)
        pimg.save(filename)
        return self

    @property
    def pil(self):
        return self.to_pilimage()

    def to_pilimage(self):
        return self.__frame_to_pil(self.__frame.copy(), self.__get_colorspace)

    @classmethod
    def from_pilimage(cls, pimg):
        frame = np.asarray(pimg)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return Image(frame)

    # ---------------------------------------------------------------------------------------
    # HSV_Lower_Yellow = (7,15,240)
    # HSV_Upper_Yellow = (30,0,255)
    # cv2 function
    def in_range(self, lower, upper):
        if not isinstance(lower, list):
            # lower = [lower, 30, 30]
            lower = [lower, 15, 240]

        if not isinstance(upper, list):
            # upper = [upper, 255, 255]
            upper = [upper, 0, 255]

        lower = np.array(lower)
        upper = np.array(upper)
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        return Image(np.copy(mask))

    def find_contours(self, min=100):
        # contours, hierarchy = cv2.findContours(self.__frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # contours, hierarchy = cv2.findContours(self.__frame, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        contours, hierarchy = cv2.findContours(
            self.__frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )
        cnts = []
        for i in range(0, len(contours)):
            if len(contours[i]) > 0:
                # remove small objects
                area = cv2.contourArea(contours[i])
                if area < min:
                    continue
                cnts.append(contours[i])
        return cnts

    def draw_contours(self, contours, txt=True):
        frame = self.__frame.copy()

        # --------------- No 1. ---------------------------------------
        # for i in range(len(contours)):
        #     area = cv2.contourArea(contours[i])
        #     cv2.drawContours(frame, [contours[i]], 0, (0, 0, 255), 2)
        #     if txt:
        #         cv2.putText(frame, f'{area}({i})', tuple(contours[i][0][0]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)

        # --------------- No 2. ---------------------------------------
        # https://webnautes.tistory.com/1270
        # 아래 부분을 함께 그려도 위의 그린 내용과 비슷하다. 일단 코멘트
        for cnt in contours:
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            cv2.drawContours(frame, [approx], 0, (0, 255, 255), 5)
        return Image(frame, self.__colorSpace)

    # def draw_contours(self, contours, txt=True):
    #     frame = self.__frame.copy()
    #     for i in range(len(contours)):
    #         box = np.int0(contours[i])
    #         cv2.drawContours(frame, [box], 0, (0, 255, 0), 3)
    #     return Image(frame, self.__colorSpace)

    def apply_mask(self, mask_img):
        img = cv2.bitwise_and(self.__frame, self.__frame, mask=mask_img.frame)
        return Image(img)

    def masking(self, mask_img):
        img = cv2.bitwise_and(self.__frame, self.__frame, mask=mask_img.frame)
        return Image(img)

    def bitwise_and(self, img, mask_img=None):
        """
        같은 shape만 적용가능
        """
        if mask_img:
            img = cv2.bitwise_and(self.__frame, img.frame, mask=mask_img.frame)
        else:
            img = cv2.bitwise_and(self.__frame, img.frame)
        return Image(img)

    def bitwise_or(self, img, mask_img=None):
        """
        같은 shape만 적용가능
        """
        if mask_img:
            img = cv2.bitwise_or(self.__frame, img.frame, mask=mask_img.frame)
        else:
            img = cv2.bitwise_or(self.__frame, img.frame)
        return Image(img)

    def bitwise_xor(self, img, mask_img):
        """
        같은 shape만 적용가능
        """
        if mask_img:
            img = cv2.bitwise_xor(self.__frame, img.frame, mask=mask_img.frame)
        else:
            img = cv2.bitwise_xor(self.__frame, img.frame)
        return Image(img)

    def bitwise_not(self):
        img = cv2.bitwise_not(self.__frame)
        return Image(img)

    # --------------------------------------------------------------------------------------
    def __color_rbg_to_bgr(self, color):
        r, g, b = color
        return (b, g, r)

    def __color_bgr_to_rgb(self, color):
        b, g, r = color
        return (r, g, b)

    # ---------------------------------------------------------------------------------------
    #  color space
    def to_rgb(self):
        frame = self.__frame.copy()
        if self.__colorSpace == ColorSpace.BGR:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif self.__colorSpace == ColorSpace.GRAY:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif self.__colorSpace == ColorSpace.HSV:
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif self.__colorSpace == ColorSpace.BGRA:
            frame = frame[:, :, (2, 1, 0, 3)]
        elif (
            self.__colorSpace == ColorSpace.RGB or self.__colorSpace == ColorSpace.RGBA
        ):
            pass

        return Image(frame, ColorSpace.RGB)

    @property
    def rgb(self):
        return self.to_rgb()

    def to_hsv(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        return Image(img, ColorSpace.HSV)

    @property
    def hsv(self):
        return self.to_hsv()

    def to_gray(self):
        frame = self.__frame.copy()
        if self.__colorSpace != ColorSpace.GRAY:
            if self.__colorSpace == ColorSpace.RGB:
                frame = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            elif self.__colorSpace == ColorSpace.BGR:
                frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            elif self.__colorSpace == ColorSpace.BGRA:
                frame = cv2.cvtColor(self.image, cv2.COLOR_BGRA2GRAY)
            elif self.__colorSpace == ColorSpace.RGBA:
                frame = cv2.cvtColor(self.image, cv2.COLOR_RGBA2GRAY)
        return Image(frame, ColorSpace.GRAY)

    @property
    def gray(self):
        return self.to_gray()

    def to_bgr(self):
        """
        hsv에서 bgr로 변환
        """
        frame = self.__frame
        if self.__colorSpace == ColorSpace.HSV:
            frame = cv2.cvtColor(self.__frame, cv2.COLOR_HSV2BGR)
        elif self.__colorSpace == ColorSpace.RGB:
            frame = cv2.cvtColor(self.__frame, cv2.COLOR_RGB2BGR)
        elif self.__colorSpace == ColorSpace.GRAY:
            frame = cv2.cvtColor(self.__frame, cv2.COLOR_GRAY2BGR)
        elif self.__colorSpace == ColorSpace.BGRA:
            frame = cv2.cvtColor(self.__frame, cv2.COLOR_BGRA2BGR)
        elif self.__colorSpace == ColorSpace.BGR:
            pass
        return Image(frame, ColorSpace.BGR)

    @property
    def bgr(self):
        return self.to_bgr()

    def to_bgra(self):
        """
        bgr에서 bgra로 변환
        """
        frame = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2BGRA)
        return Image(frame, ColorSpace.BGRA)

    @property
    def bgra(self):
        return self.to_bgra()

    def split(self, ch="r"):
        if ch == "r":
            b, g, r = cv2.split(self.__frame)
            return Image(r, ColorSpace.GRAY)
        elif ch == "g":
            b, g, r = cv2.split(self.__frame)
            return Image(g, ColorSpace.GRAY)
        elif ch == "b":
            b, g, r = cv2.split(self.__frame)
            return Image(b, ColorSpace.GRAY)
        elif ch == "a":
            if self.__colorSpace == ColorSpace.BGRA:
                b, g, r, a = cv2.split(self.__frame)
                return Image(a, ColorSpace.GRAY)
        return None

    def threshold(self, thresh=127, maxv=255):
        _, frame = cv2.threshold(self.__frame, value, 255, cv2.THRESH_BINARY)
        return Image(frame, ColorSpace.GRAY)

    def binarize(self, value):
        frame = self.to_gray().frame
        _, frame = cv2.threshold(frame, value, 255, cv2.THRESH_BINARY)
        return Image(frame, ColorSpace.GRAY)

    def invert(self):
        img = cv2.bitwise_not(self.__frame)
        return Image(img, ColorSpace.GRAY)

    def blit(self, x, y, img):
        if self.__colorSpace == ColorSpace.GRAY:
            print("GRAY 이미지에는 오버레이 할 수 없습니다")
            return Image(np.copy(self.__frame), ColorSpace.GRAY)

        h, w, c = img.frame.shape
        if c == 4:
            frame = self.__transparent_overlay(img, pos=(x, y))
            return Image(frame, self.__colorSpace)
        elif c == 3:
            frame = np.copy(self.__frame)
            frame[y : y + h, x : x + w] = img.frame
            return Image(frame, self.__colorSpace)
        else:
            print("GRAY 이미지에는 오버레이 할 수 없습니다")
            return Image(np.copy(self.__frame), ColorSpace.GRAY)

    def overlay(self, x, y, img):
        # blit()함수와 같은데.
        if self.__colorSpace == ColorSpace.GRAY:
            print("GRAY 이미지에는 오버레이 할 수 없습니다")
            return Image(np.copy(self.__frame), ColorSpace.GRAY)

        h, w, c = img.frame.shape
        if c == 4:
            frame = self.__transparent_overlay(img, pos=(x, y))
            return Image(frame, self.__colorSpace)
        elif c == 3:
            frame = np.copy(self.__frame)
            frame[y : y + h, x : x + w] = img.frame
            return Image(frame, self.__colorSpace)
        else:
            print("GRAY 이미지에는 오버레이 할 수 없습니다")
            return Image(np.copy(self.__frame), ColorSpace.GRAY)

    def __transparent_overlay(self, overlay, pos=(0, 0), scale=1):
        """
        투명 이미지(BGRA)를 오버레이 한다.
        :param overlay: 투명 Image (BGRA)
        :param pos:  위치.
        :param scale : 스케일.
        :return: Image
        """
        src = np.copy(self.__frame)
        overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
        h, w, _ = overlay.shape  # Size of foreground
        rows, cols, _ = src.shape  # Size of background Image
        y, x = pos[0], pos[1]  # Position of foreground/overlay image

        # loop over all pixels and apply the blending equation
        for i in range(h):
            for j in range(w):
                if x + i >= rows or y + j >= cols:
                    continue
                alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
                src[x + i][y + j] = (
                    alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
                )
        return src

    def blend(self, img, weight):
        frame = cv2.addWeighted(self.__frame, 1 - weight, img.frame, weight, 0)
        return Image(frame)

    def blur(self, x, y, w, h, ksize=30):
        frame = np.copy(self.__frame)
        if w > 0 and h > 0:
            roi = frame[y : y + h, x : x + w]
            roi = cv2.blur(roi, (ksize, ksize))
            frame[y : y + h, x : x + w] = roi
        return Image(frame, self.__colorSpace)

    # ---------------------------------------------------------------------------------------
    #  static method
    @classmethod
    def merge(cls, b, g, r):
        frame = cv2.merge((b.frame, g.frame, r.frame))
        return Image(frame, ColorSpace.BGR)

    @classmethod
    def load(cls, filename):
        if re.match(r"\w+://", filename):
            with urllib.request.urlopen(filename) as url:
                f = io.BytesIO(url.read())
                pil_image = PImage.open(f)
        else:
            # 한글 파일명이 있으면 cv2.imread는 못 읽어들인다.그래서 PImage
            pil_image = PImage.open(filename)

        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return Image(frame).set_filename(filename)

    @classmethod
    def open(cls, filename):
        return cls.load(filename)

    @classmethod
    def concatenate(cls, img1, img2, axis="h"):
        """
        'h' : horizontal
        'v' : vertical
        """
        if axis == "v":
            axis = 0
        else:
            axis = 1
        frame = np.concatenate((img1.frame, img2.frame), axis=axis)
        return Image(frame)

    def bounding_rect(self, cnts, draw=False):
        """Contours의 영역을 포함하는 최소의 영역을 구한다.

        Args:
            cnts (list): Contours의 리스트

        Returns:
            list: 바운딩 박스 리스트 (x1, y1, x2, y2)
        """
        # http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html

        # https://webnautes.tistory.com/1270
        frame = self.__frame.copy()
        rects = []
        for i in range(0, len(cnts)):
            if len(cnts[i]) > 0:
                x, y, w, h = cv2.boundingRect(cnts[i])
                rects.append([x, y, x + w, y + h])

        if draw:
            for bb in rects:
                (x1, y1, x2, y2) = bb
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
            self.__frame = frame
        return rects

    @classmethod
    def empty(cls, size, color=Color.DEFAULT, width=0, height=0):
        """지정한 크기의 이미지를 만든다.

        Args:
            size (tuple): (w, h)
            weight (int): 이미지의 넓이
            height (int): 이미지의 높이
            color (tuple): (r, g, b) 값

        Returns:
            Image: 만들어진 이미지 객체
        """
        if size and isinstance(size, tuple):
            width, height = size
        if width == 0 or height == 0:
            height = builtins.HEIGHT
            width = builtins.WIDTH
        frame = np.zeros((height, width, 3), np.uint8)
        frame[:, :] = color[::-1]
        return Image(frame)

    @classmethod
    def fromarray(cls, arr, colorspace=ColorSpace.BGR):
        if not isinstance(arr, np.ndarray):
            arr = np.array(arr, dtype="uint8")

        if len(arr.shape) == 2:
            return Image(arr, ColorSpace.GRAY)
        else:
            return Image(arr, colorspace)

    def empty_like(self, color=(255, 255, 255)):
        """이미지와 같은 차원(shape)의 주어진 색상의 이미지 만든다.

        Args:
            color (tuple, optional): (r, g, b)값. Defaults to (255, 255, 255).

        Returns:
            Image: 만들어진 이미지 객체
        """
        frame = np.zeros(self.__frame.shape, np.uint8)
        return Image(frame)

    def background(self, color):
        """이미지 전체를 주어진 색상으로 바꾼다

        Args:
            color (tuple): (r, g, b) 색상값

        Returns:
            Image: 만들어진 이미지 객체
        """
        frame = self.__frame.copy()
        frame[:, :] = color[::-1]
        return Image(frame)

    def __is_number(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return True
        else:
            return False

    #
    # https://docs.python.org/ko/3.7/library/operator.html
    #
    def pixel(self, x=0, y=0):
        """
        return (r, g, b)
        """
        pixel = self.__frame[y, x]
        pixel = pixel.tolist()
        if self.__colorSpace == ColorSpace.BGR:
            pixel = pixel[::-1]  # bgr- > rgb
        return tuple(pixel)

    # img[:,:,::-1] brg -> rgb,
    def __getitem__(self, coord):
        """
        coord is (x, y)
        """
        # coord -> (x, y)

        x, y = coord
        if isinstance(x, int) and isinstance(y, int):
            return self.pixel(x, y)
        elif isinstance(x, slice) and isinstance(y, slice):
            pixel = self.__frame[y, x]
            return Image(pixel)
        else:
            return None

    def __setitem__(self, coord, value):
        """
        coord  is (x, y)
        value is (r, g, b)
        """
        # coord -> (x, y)
        x, y = coord
        if self.__colorSpace == ColorSpace.RGB:
            self.__image[(y, x)] = value
        else:
            self.__image[(y, x)] = value[::-1]

    def __bool__(self):
        if isinstance(self.image, np.ndarray):
            return True
        return False

    def __repr__(self):
        return f"<HelloAI.Image Object Shape:{self.__frame.shape}, Color:({self.__colorSpace}) ,at memory location: ({hex(id(self))})>"

    def __add__(self, other):
        self_frame = self.__frame
        other_frame = other.frame

        if self.__is_number(other):
            other = cv2.add(self.__frame, other)
        else:
            if len(self_frame.shape) != len(other_frame.shape):
                print("두 이미지의 컬러 채널이 다릅니다")
                return None

            other = cv2.add(self_frame, other_frame)
        return Image(other, ColorSpace.BGR)

    def diff(self, img):
        frame = self.__frame.copy()
        other = img.frame.copy()
        diff = cv2.absdiff(frame, other)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)

        return Image(dilated, ColorSpace.GRAY)

    def __sub__(self, other):
        if self.__is_number(other):
            other = cv2.subtract(self.__frame, other)
        else:
            # if self.__colorSpace != other.colorspace:
            #     return None
            other = cv2.subtract(self.__frame, other.frame)
        return Image(other)

    def __div__(self, other):
        if self.__is_number(other):
            other = cv2.divide(self.__frame, other)
        return Image(other)

    def __truediv__(self, other):
        if self.__is_number(other):
            other = cv2.divide(self.__frame, other)
            other = other.astype(np.uint8)
        return Image(other)

    def __floordiv__(self, other):
        if self.__is_number(other):
            other = cv2.divide(self.__frame, other)
            other = other.astype(np.uint8)
        return Image(other)

    def __mul__(self, other):
        if self.__is_number(other):
            other = cv2.multiply(self.__frame, other)
        return Image(other)

    def __neg__(self):
        """
        -obj
        """
        return self.invert()

    def __invert__(self):
        """
        ~obj
        """
        return self.invert()

    # 음...제대로 동작하지 않는다..
    #  BLOB(Binary Large Object)는 이진 스케일로 연결된 픽셀 그룹을 말합니다
    def __find_blobs(self, min_area=200, draw=False):
        frame = np.copy(self.__frame)
        if self.__colorSpace == ColorSpace.BGR:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif self.__colorSpace == ColorSpace.RGB:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        elif self.__colorSpace == ColorSpace.GRAY:
            gray = frame
        else:
            return

        cv2.imshow("blob", gray)

        # blob 검출 필터 파라미터 생성
        params = cv2.SimpleBlobDetector_Params()

        # 경계값 조정
        params.minThreshold = 10
        params.maxThreshold = 240
        params.thresholdStep = 5
        # 면적 필터 켜고 최소 값 지정
        params.filterByArea = True
        params.minArea = min_area

        # 컬러, 볼록 비율, 원형비율 필터 옵션 끄기
        params.filterByColor = False
        params.filterByConvexity = False
        params.filterByInertia = False
        params.filterByCircularity = False

        # 필터 파라미터로 blob 검출기 생성
        detector = cv2.SimpleBlobDetector_create(params)
        # 키 포인트 검출
        keypoints = detector.detect(gray)
        # 키 포인트 그리기
        if draw:
            frame = cv2.drawKeypoints(
                frame, keypoints, None, None, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )

        # 결과 출력
        return Image(frame, self.__colorSpace), keypoints

    # https://jvvp.tistory.com/1081
    def erode(self, kernelsize=3, iterations=1):
        kernel = {}
        kernel[0] = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
        kernel[1] = cv2.getStructuringElement(cv2.MORPH_CROSS, (kernelsize, kernelsize))
        kernel[2] = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (kernelsize, kernelsize)
        )

        if self.__colorSpace != ColorSpace.GRAY:
            return None

        frame = cv2.erode(frame, kernel[0], iterations=iterations)
        return Image(frame, ColorSpace.GRAY)

    # https://jvvp.tistory.com/1081
    def dilate(self, kernelsize=3, iterations=1):
        kernel = {}
        kernel[0] = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
        kernel[1] = cv2.getStructuringElement(cv2.MORPH_CROSS, (kernelsize, kernelsize))
        kernel[2] = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (kernelsize, kernelsize)
        )

        if self.__colorSpace != ColorSpace.GRAY:
            return None

        frame = cv2.dilate(frame, kernel[0], iterations=iterations)
        return Image(frame, ColorSpace.GRAY)

    def color_distance(self, color=(0, 0, 0)):
        """
        color is (r, g, b)
        """
        frame = self.__frame.copy()

        # color rgb -> bgr
        color = color[::-1]
        # frame = frame[:, :, ::-1].transpose([1, 0, 2])
        distances = spsd.cdist(
            frame.reshape(-1, 3), [color]
        )  # calculate the distance each pixel is

        distances *= 255.0 / distances.max()  # normalize to 0 - 255
        distances = distances.astype(np.uint8)
        frame = distances.reshape(self.__height, self.__width)
        return Image(frame, ColorSpace.GRAY)

    def flatten(self):
        return self.__frame.copy().flatten(order="C")

    # ------------
    # show 함수를 위해서 window 클래스와 중복된 처리
    def show(self, title=None):
        self.__is_notebook = is_notebook() or is_colab()
        self.__wnd_name = None
        frame = self.__frame.copy()
        if self.__is_notebook:
            # plt.imshow(frame)
            plt.imshow(np.array(frame))
        else:
            if len(builtins.windows) > 5:
                print("열려있는 창이 너무 많습니다")
                raise Exception("열려있는 창이 너무 많습니다")

            if not title:
                self.__wnd_name = str(uuid.uuid4()).split("-")[0]
            else:
                self.__wnd_name = title

            cv2.namedWindow(self.__wnd_name)
            # cv2.imshow(self.__wnd_name, self.__frame)
            cv2.setMouseCallback(self.__wnd_name, self.mouse_event)
            if self.__add_window():
                cv2.imshow(self.__wnd_name, self.__frame)

    def mouse_event(self, event, x, y, flags, params):
        if builtins.mouse_event:
            builtins.mouse_event(self.__wnd_name, event, x, y, flags, params)

    def __add_window(self):
        if self.__wnd_name not in builtins.windows:
            builtins.windows.append(self.__wnd_name)
        return True

    def __remove_window(self):
        if self.__wnd_name not in builtins.windows:
            builtins.windows.remove(self.__wnd_name)

    def to_pilimage(self):
        frame = self.__frame.copy()
        if self.__colorSpace == ColorSpace.BGR:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pimg = PImage.fromarray(frame)
        return pimg

    @property
    def pilimage(self):
        return self.to_pilimage()

    @classmethod
    def from_pilimage(cls, pimg):
        frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
        return Image(frame)

    def point(self, x, y, color=Color.RED):
        pimg = self.__frame_to_pil(self.__frame.copy(), self.__colorSpace)
        draw = ImageDraw.Draw(pimg)
        draw.point((x, y), fill=color)
        frame = self.__pil_to_frame(pimg)
        return Image(frame, self.__colorSpace)

    def line(self, start, end, color=Color.RED, thickness=1):

        pimg = self.__frame_to_pil(self.__frame.copy(), self.__colorSpace)
        draw = ImageDraw.Draw(pimg)
        draw.line([start[0], start[1], end[0], end[1]], fill=color, width=thickness)
        frame = self.__pil_to_frame(pimg)
        return Image(frame, self.__colorSpace)

    def __line(self, start, end, color=Color.RED, thickness=1):
        # 이미지를 직접 업데이트한다.
        pimg = self.__frame_to_pil(self.__frame.copy(), self.__colorSpace)
        draw = ImageDraw.Draw(pimg)
        draw.line([start[0], start[1], end[0], end[1]], fill=color, width=thickness)
        frame = self.__pil_to_frame(pimg)
        self.__frame = frame
        return Image(self.__frame, self.__colorSpace)

    def rectangle(self, start, end, outline=(0, 0, 0), fill=None, thickness=1):
        (x1, y1) = start
        (x2, y2) = end

        pimg = self.__frame_to_pil(self.__frame.copy(), self.__colorSpace)
        draw = ImageDraw.Draw(pimg, "RGBA")
        draw.rectangle(
            ((x1, y1), (x2, y2)), outline=outline, width=thickness, fill=fill
        )

        frame = self.__pil_to_frame(pimg, self.__colorSpace)

        return Image(frame, self.__colorSpace)

    def rect(self, start, end, outline=(0, 0, 0), fill=None, thickness=1):
        return self.rectangle(start, end, outline, fill, thickness)

    def ellipse(self, xy, width, height, fill=None, outline=(0, 0, 0), thickness=1):
        x, y = xy
        x1 = int(x - (width / 2))
        y1 = int(y - (height / 2))
        x2 = int(x + (width / 2))
        y2 = int(y + (height / 2))
        pimg = self.__frame_to_pil(self.__frame.copy(), self.__colorSpace)
        draw = ImageDraw.Draw(pimg, "RGBA")
        draw.ellipse([x1, y1, x2, y2], fill=fill, outline=outline, width=thickness)
        frame = self.__pil_to_frame(pimg)
        return Image(frame, self.__colorSpace)

    def arc(self, x, y, width, height, start, end, fill=None, thickness=1):
        x1 = int(x - (width / 2))
        y1 = int(y - (height / 2))
        x2 = int(x + (width / 2))
        y2 = int(y + (height / 2))
        pimg = self.__frame_to_pil(self.__frame.copy(), self.__get_colorspace)
        draw = ImageDraw.Draw(pimg)
        draw.arc([x1, y1, x2, y2], start=start, end=end, fill=fill, width=thickness)
        frame = self.__pil_to_frame(pimg)
        return Image(frame, self.__colorSpace)

    def chord(
        self, x, y, width, height, start, end, fill=None, outline=None, thickness=1
    ):
        x1 = int(x - (width / 2))
        y1 = int(y - (height / 2))
        x2 = int(x + (width / 2))
        y2 = int(y + (height / 2))
        pimg = self.__frame_to_pil(self.__frame.copy(), self.__get_colorspace)
        draw = ImageDraw.Draw(pimg)
        draw.arc(
            [x1, y1, x2, y2],
            start=start,
            end=end,
            fill=fill,
            outline=outline,
            width=thickness,
        )
        frame = self.__pil_to_frame(pimg)
        return Image(frame, self.__colorSpace)

    # [(x, y), (x, y), ...]
    def polygon(self, points, fill=None, outline=None):
        pimg = self.__frame_to_pil(self.__frame.copy(), self.__get_colorspace)
        draw = ImageDraw.Draw(pimg)
        draw.polygon(points, fill=fill, outline=outline)
        frame = self.__pil_to_frame(pimg)
        return Image(frame, self.__colorSpace)

    # https://qiita.com/mo256man/items/82da5138eeacc420499d
    def text(self, xy, text="HelloAI", size=14, color=(0, 0, 0)):
        """
        color = (r,g,b)
        """
        # PIL로 저장해서 한글 표시
        x, y = xy
        FONT_PATH = "./assets/fonts/gulim.ttc"
        pimg = self.__frame_to_pil(self.__frame.copy(), self.__get_colorspace)
        draw = ImageDraw.Draw(pimg)
        font_ttf = ImageFont.truetype(font=FONT_PATH, size=size)  # TrueType（TTF）
        draw.text(xy=(x, y), text=text, fill=color, font=font_ttf)
        frame = self.__pil_to_frame(pimg)
        
        return Image(frame, self.__colorSpace)

    # -----------------------------------------------------------------------------------------


class ImageSet:
    def __init__(self, path):
        self.__path = path
        if not os.path.exists(path):
            raise Exception("폴더가 존재하지 않습니다. " + path)

        self.__files = glob(os.path.join(path, "*.*"))

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.__files) > 0:
            file_path = self.__files.pop()
            img = Image.load_image(file_path)
            return img
        else:
            raise StopIteration

    def __len__(self):
        return len(self.__files)
