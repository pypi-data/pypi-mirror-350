import builtins
import sys
import os
import time
import cv2
import numpy as np
import uuid

from PIL import Image as pilImage
from PIL import ImageDraw
from PIL import ImageFont


from helloai.core.image import Image, ColorSpace
from helloai.core.singlestore import SingleStore
from helloai.core.config import *
from helloai.core.colors import *


__all__ = ["Window"]


# DEFAULT_HEIGHT= 480
# DEFAULT_WIDTH = 480
# INIT_DISPLAY = cv2.putText(np.zeros((DEFAULT_HEIGHT, DEFAULT_WIDTH, 3)),
#                            'HelloAI', (5, 15), cv2.FONT_HERSHEY_TRIPLEX,
#                            0.5, (0, 255, 255), 1, cv2.LINE_AA)


class Window:
    def __init__(self, name=None, size=(640, 480)):
        self.__image = None
        if name is not None:
            self.__name = name.replace(" ", "-")
        else:
            self.__name = str(uuid.uuid4()).split("-")[0]

        builtins.WIDTH = size[0]
        builtins.HEIGHT = size[1]

        self.singlestore = SingleStore()
        self.__image = self.__create_default_image()
        cv2.namedWindow(self.__name)
        cv2.imshow(self.__name, self.__image.frame)
        cv2.setMouseCallback(self.__name, self.mouse_event)
        self.__add_window()
        

    def __repr__(self):
        return f"<HelloAI.Window Object Title:{self.__name}, Size:({self.size}) ,at memory location: ({hex(id(self))})>"

    def __add_window(self):
        if self.__name not in builtins.windows:
            builtins.windows.append(self.__name)

    def __remove_window(self):
        if self.__name in builtins.windows:
            builtins.windows.remove(self.__name)

    def __create_default_image(self):
        frame = np.zeros((builtins.HEIGHT, builtins.WIDTH, 3))
        frame[:, :] = Color.LIGHTGRAY
        frame = frame.astype(np.uint8)
        return Image(frame)

    def mouse_event(self, event, x, y, flags, params):
        # if self.singlestore.mouse_event:
        #     self.singlestore.mouse_event(self.__name, event, x, y, flags, params)
        if builtins.mouse_event:
            builtins.mouse_event(self.__name, event, x, y, flags, params)

    def show(self, img=None):
        # RGB 이미지가 정상 표시되도록
        if img:
            self.__image = img
        frame = self.__image.frame.copy()
        cv2.imshow(self.__name, frame)

    def update(self, img):
        self.show(img)

    def save(self, path, name=None):
        """
        jpg파일로 저장
        """
        if path != None and path.endswith("/"):
            path = path[:-1]

        if not os.path.isdir(path):
            os.mkdir(path)

        if not name:
            name = str(round(time.time() * 1000))

        filename = f"{path}/{name}.jpg"
        cv2.imwrite(filename, self.__image.frame)

    @property
    def image(self):
        return self.__image.copy()

    @property
    def name(self):
        return self.__name

    @property
    def size(self):
        return (self.__image.frame.shape[1], self.__image.frame.shape[0])

    @property
    def width(self):
        return self.__image.frame.shape[1]
    
    @property
    def width_(self):
        return self.__image.frame.shape[1]

    @property
    def height(self):
        return self.__image.frame.shape[0]
    
    @property
    def height_(self):
        return self.__image.frame.shape[0]

    def close(self):
        cv2.destroyWindow(self.__name)
        self.__remove_window()
        if len(builtins.windows) == 0:
            sys.exit()

    # ---------------------------------------------------------------------------------------------
    # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.arc
    def point(self, x, y, color=Color.RED):
        pimg = self.__image.to_pilimage()
        draw = ImageDraw.Draw(pimg)
        draw.point((x, y), fill=color)
        img = Image.from_pilimage(pimg)
        self.__image = img
        # cv2.imshow(self.__name, img.frame)

    def line(self, start, end, color=Color.RED, thickness=1):
        pimg = self.__image.to_pilimage()
        draw = ImageDraw.Draw(pimg)
        draw.line([start[0], start[1], end[0], end[1]], fill=color, width=thickness)
        img = Image.from_pilimage(pimg)
        self.__image = img

    def rectangle(self, start, end, outline=(0, 0, 0), fill=None, thickness=1):
        (x1, y1) = start
        (x2, y2) = end

        pimg = self.__image.to_pilimage()
        draw = ImageDraw.Draw(pimg)
        draw.rectangle(
            ((x1, y1), (x2, y2)), outline=outline, width=thickness, fill=fill
        )
        img = Image.from_pilimage(pimg)
        self.__image = img
        return self

    def ellipse(self, xy, width, height, fill=None, outline=(0, 0, 0), thickness=1):
        x, y = xy
        x1 = int(x - (width / 2))
        y1 = int(y - (height / 2))
        x2 = int(x + (width / 2))
        y2 = int(y + (height / 2))
        pimg = self.__image.to_pilimage()
        draw = ImageDraw.Draw(pimg)
        draw.ellipse([x1, y1, x2, y2], fill=fill, outline=outline, width=thickness)
        img = Image.from_pilimage(pimg)
        self.__image = img

    def arc(self, x, y, width, height, start, end, fill=None, thickness=1):
        x1 = int(x - (width / 2))
        y1 = int(y - (height / 2))
        x2 = int(x + (width / 2))
        y2 = int(y + (height / 2))
        pimg = self.__image.to_pilimage()
        draw = ImageDraw.Draw(pimg)
        draw.arc([x1, y1, x2, y2], start=start, end=end, fill=fill, width=thickness)
        img = Image.from_pilimage(pimg)
        self.__image = img

    def chord(
        self, x, y, width, height, start, end, fill=None, outline=None, thickness=1
    ):
        x1 = int(x - (width / 2))
        y1 = int(y - (height / 2))
        x2 = int(x + (width / 2))
        y2 = int(y + (height / 2))
        pimg = self.__image.to_pilimage()
        draw = ImageDraw.Draw(pimg)
        draw.arc(
            [x1, y1, x2, y2],
            start=start,
            end=end,
            fill=fill,
            outline=outline,
            width=thickness,
        )
        img = Image.from_pilimage(pimg)
        self.__image = img

    # [(x, y), (x, y), ...]
    def polygon(self, points, fill=None, outline=None):
        pimg = self.__image.to_pilimage()
        draw = ImageDraw.Draw(pimg)
        draw.polygon(points, fill=fill, outline=outline)
        img = Image.from_pilimage(pimg)
        self.__image = img

    # https://qiita.com/mo256man/items/82da5138eeacc420499d
    def text(self, xy, text="HelloAI", size=14, color=(0, 0, 0)):
        """
        color = (r,g,b)
        """
        # PIL로 저장해서 한글 표시
        x, y = xy
        FONT_PATH = "./assets/fonts/gulim.ttc"
        pimg = self.__image.to_pilimage()
        draw = ImageDraw.Draw(pimg)
        font_ttf = ImageFont.truetype(font=FONT_PATH, size=size)  # TrueType（TTF）
        draw.text(xy=(x, y), text=text, fill=color, font=font_ttf)
        img = Image.from_pilimage(pimg)
        self.__image = img

    def background(self, color):
        """윈도우 배경색상을 바꾼다.

        Args:
            color (int or tuple): 색상 (r, g, b)

        Returns:
            None
        """
        if isinstance(color, int):
            color = (color, color, color)
        elif isinstance(color, tuple):
            if len(color) == 1:
                color = (color[0], color[0], color[0])
            elif len(color) == 3:
                pass
            elif len(color) == 4:
                color = (color[0], color[1], color[0])
        self.__image.frame[:, :] = color[::-1]
