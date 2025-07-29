import builtins
import cv2
import requests
import numpy as np
import time
from urllib.parse import urlparse

from .image import Image

__all__ = ["VirtualCamera"]


class VirtualCamera:
    """
    flip: 1 좌우, 0 상하 반전
    """

    def __init__(self, url, flip=True):
        if not url.startswith("http://") and not url.startswith("https://"):
            print("카메라의 주소가 잘못되었습니다")

        self.__url = url
        self.__flip = flip
        self.__width = builtins.WIDTH
        self.__height = builtins.HEIGHT
        self.__channel = 3
        self.__type = None
        self.__capture = None
        self.__frame = np.zeros((self.__height, self.__width, self.__channel))

        if "videostream.cgi" in self.__url:
            # kamibot ai camera
            self.__type = "ai"
            if "@" not in self.__url:
                parts = urlparse(self.__url)
                # "http://192.168.66.1:9527/videostream.cgi"
                # parts- ParseResult(scheme='http', netloc='192.168.66.1:9527', path='/videostream.cgi', params='', query='', fragment='')
                self.__url = f"{parts.scheme}://admin:admin@{parts.netloc}{parts.path}"
                # url = "http://admin:admin@192.168.66.1:9527/videostream.cgi"
                self.__capture = cv2.VideoCapture(self.__url)
                time.sleep(1)  # 1sec 카메라가 인식될때 시간이 조금 필요
        else:
            self.__type = "app"

    def read(self):
        if self.__type == "ai":
            return self.__read_from_aicamera()
        else:
            return self.__read_from_app()

    def __read_from_aicamera(self):
        ret, frame = self.__capture.read()
        if ret:
            self.__frame = frame
        return Image(frame)

    def __read_from_app(self):
        try:
            r = requests.get(self.__url, stream=True)
        except:
            print("카메라 서버에 문제가 있습니다")
            return Image(self.__frame)

        if r.status_code == 200:
            bytes = b""
            for chunk in r.iter_content(chunk_size=1024):
                bytes += chunk
                a = bytes.find(b"\xff\xd8")
                b = bytes.find(b"\xff\xd9")
                if a != -1 and b != -1:
                    jpg = bytes[a : b + 2]
                    bytes = bytes[b + 2 :]
                    frame = cv2.imdecode(
                        np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR
                    )
                    if self.__flip:
                        frame = cv2.flip(frame, 1)  # 1 좌우, 0 상하 반전
                        self.__frame = frame
        return Image(self.__frame)
